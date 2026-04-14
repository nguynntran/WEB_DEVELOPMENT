from flask import render_template, request, redirect, flash
from app.models import db, Tournament, Team, Match, Result, Standing
from flask_login import login_required, current_user
from datetime import datetime


def recalculate_standings(tournament_id):
    """Recalculate standings for a tournament based on match results"""
    teams = Team.query.filter_by(tournament_id=tournament_id).all()

    Standing.query.filter_by(tournament_id=tournament_id).delete()

    table = {}
    for team in teams:
        table[team.id] = {
            'points': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0
        }

    matches = Match.query.filter_by(tournament_id=tournament_id).all()
    for match in matches:
        if not match.result:
            continue

        team1_id = match.team1_id
        team2_id = match.team2_id
        team1_score = match.result.team1_score
        team2_score = match.result.team2_score

        if team1_score > team2_score:
            table[team1_id]['wins'] += 1
            table[team1_id]['points'] += 3
            table[team2_id]['losses'] += 1
        elif team2_score > team1_score:
            table[team2_id]['wins'] += 1
            table[team2_id]['points'] += 3
            table[team1_id]['losses'] += 1
        else:
            table[team1_id]['draws'] += 1
            table[team2_id]['draws'] += 1
            table[team1_id]['points'] += 1
            table[team2_id]['points'] += 1

    for team in teams:
        row = table[team.id]
        standing = Standing(
            tournament_id=tournament_id,
            team_id=team.id,
            points=row['points'],
            wins=row['wins'],
            losses=row['losses'],
            draws=row['draws']
        )
        db.session.add(standing)


def register_match_routes(app, db):
    """Register match routes to the Flask app"""

    @app.route('/matches', endpoint='matches')
    @login_required
    def matches():
        """List all matches for user's tournaments"""
        tournament_id = request.args.get('tournament_id')

        user_tournaments = Tournament.query.filter_by(creator_id=current_user.id).order_by(Tournament.name.asc()).all()
        query = Match.query.join(Tournament).filter(Tournament.creator_id == current_user.id)

        selected_tournament = None
        if tournament_id:
            query = query.filter(Match.tournament_id == tournament_id)
            selected_tournament = Tournament.query.filter_by(id=tournament_id, creator_id=current_user.id).first()

        all_matches = query.order_by(Match.round.asc(), Match.id.asc()).all()
        return render_template(
            'matches/matches.html',
            matches=all_matches,
            tournaments=user_tournaments,
            selected_tournament=selected_tournament
        )

    @app.route('/matches/<id>/result', methods=['GET', 'POST'], endpoint='match_result')
    @login_required
    def match_result(id):
        """Submit or edit match result"""
        match = Match.query.get_or_404(id)

        if match.tournament.creator_id != current_user.id:
            flash('You are not allowed to update this match.')
            return redirect('/matches')

        existing_result = Result.query.filter_by(match_id=match.id).first()

        if request.method == 'POST':
            scheduled_time_str = request.form.get('scheduled_time')
            team1_score_str = request.form.get('team1_score')
            team2_score_str = request.form.get('team2_score')

            try:
                if scheduled_time_str:
                    match.scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')

                team1_score = int(team1_score_str)
                team2_score = int(team2_score_str)
                if team1_score < 0 or team2_score < 0:
                    flash('Scores must be 0 or greater.')
                    return redirect(f'/matches/{id}/result')

                winner_id = None
                if team1_score > team2_score:
                    winner_id = match.team1_id
                elif team2_score > team1_score:
                    winner_id = match.team2_id

                if existing_result:
                    existing_result.team1_score = team1_score
                    existing_result.team2_score = team2_score
                    existing_result.winner_id = winner_id
                    existing_result.submitted_by = current_user.id
                else:
                    new_result = Result(
                        match_id=match.id,
                        team1_score=team1_score,
                        team2_score=team2_score,
                        winner_id=winner_id,
                        submitted_by=current_user.id
                    )
                    db.session.add(new_result)

                match.status = 'completed'
                recalculate_standings(match.tournament_id)
                db.session.commit()

                flash('Match result saved successfully!')
                return redirect(f'/matches?tournament_id={match.tournament_id}')
            except ValueError:
                flash('Invalid input. Please enter valid score numbers and date/time.')
                return redirect(f'/matches/{id}/result')

        return render_template('matches/matches_result.html', match=match, result=existing_result)
