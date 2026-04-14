from flask import render_template, request
from app.models import db, Tournament, Team, Match, Standing
from flask_login import login_required, current_user


def recalculate_standings_view(tournament_id):
    """Recalculate standings for a tournament"""
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


def register_standing_routes(app, db):
    """Register standing routes to the Flask app"""

    @app.route('/standings', endpoint='standings')
    @login_required
    def standings():
        """View standings for tournaments"""
        tournament_id = request.args.get('tournament_id')

        user_tournaments = Tournament.query.filter_by(
            creator_id=current_user.id
        ).order_by(Tournament.name.asc()).all()

        selected_tournament = None
        standings_rows = []

        if tournament_id:
            selected_tournament = Tournament.query.filter_by(
                id=tournament_id,
                creator_id=current_user.id
            ).first()

            if selected_tournament:
                recalculate_standings_view(selected_tournament.id)
                db.session.commit()
                standings_rows = Standing.query.join(Team).filter(
                    Standing.tournament_id == selected_tournament.id
                ).order_by(
                    Standing.points.desc(),
                    Standing.wins.desc(),
                    Standing.draws.desc(),
                    Standing.losses.asc(),
                    Team.name.asc()
                ).all()

        return render_template(
            'standings/standings.html',
            tournaments=user_tournaments,
            selected_tournament=selected_tournament,
            standings=standings_rows
        )
