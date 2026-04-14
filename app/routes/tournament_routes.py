from flask import render_template, request, redirect, flash
from app.models import db, Tournament, Team, Match
from flask_login import login_required, current_user
from datetime import datetime


def generate_round_robin_matches(tournament):
    """Generate round robin matches for a tournament"""
    teams = Team.query.filter_by(tournament_id=tournament.id).order_by(Team.id).all()
    if len(teams) < 2:
        return 0

    team_ids = [team.id for team in teams]
    if len(team_ids) % 2 == 1:
        team_ids.append(None) 

    total_rounds = len(team_ids) - 1
    half = len(team_ids) // 2
    created_count = 0

    for round_num in range(total_rounds):
        for i in range(half):
            team1_id = team_ids[i]
            team2_id = team_ids[-(i + 1)]

            if team1_id is not None and team2_id is not None:
                match = Match(
                    tournament_id=tournament.id,
                    team1_id=team1_id,
                    team2_id=team2_id,
                    round=f'Round {round_num + 1}',
                    status='scheduled'
                )
                db.session.add(match)
                created_count += 1

        # Circle method rotation 
        team_ids = [team_ids[0]] + [team_ids[-1]] + team_ids[1:-1]

    return created_count


def generate_knockout_matches(tournament):
    """Generate knockout matches for a tournament"""
    teams = Team.query.filter_by(tournament_id=tournament.id).order_by(Team.id).all()
    if len(teams) < 2:
        return 0

    created_count = 0
    for i in range(0, len(teams) - 1, 2):
        match = Match(
            tournament_id=tournament.id,
            team1_id=teams[i].id,
            team2_id=teams[i + 1].id,
            round='Round 1',
            status='scheduled'
        )
        db.session.add(match)
        created_count += 1

    return created_count


def register_tournament_routes(app, db):
    """Register tournament routes to the Flask app"""

    @app.route('/tournaments', endpoint='tournaments')
    def tournaments():
        """List all tournaments created by current user"""
        all_tournaments = Tournament.query.filter_by(creator_id=current_user.id).order_by(Tournament.start_date.desc()).all()
        return render_template('tournament/tournaments.html', tournaments=all_tournaments)

    @app.route('/tournaments/create', methods=['GET', 'POST'], endpoint='create_tournament')
    @login_required
    def create_tournament():
        """Create a new tournament"""
        if request.method == 'GET':
            return render_template('tournament/create_tournament.html')
        elif request.method == 'POST':
            name = request.form.get('name')
            sport_type = request.form.get('sport_type')
            format = request.form.get('format')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                if end_date < start_date:
                    flash("ERROR: End date must be after start date")
                    return redirect('/tournaments/create')
                new_tournament = Tournament(
                name=name,
                sport_type=sport_type,
                format=format,
                start_date=start_date,
                end_date=end_date,
                creator_id=current_user.id
                )
                db.session.add(new_tournament)
                db.session.commit()
                
                print(f"Created tournament: {new_tournament} + with ID {new_tournament.id} - Name: {new_tournament.name}")
                flash("Tournament created successfully!")
                return redirect('/tournaments')
            except ValueError:
                flash("ERROR: Invalid date format. Please use YYYY-MM-DD.")
                return redirect('/tournaments/create')

    @app.route('/tournaments/<id>', endpoint='tournament_detail')
    @login_required
    def tournament_detail(id):
        """View tournament details"""
        tournament = Tournament.query.get_or_404(id)
        teams = tournament.teams
        return render_template('tournament/tournament_detail.html', tournament=tournament, teams=teams)

    @app.route('/tournaments/<id>/edit', methods=['GET', 'POST'], endpoint='edit_tournament')
    @login_required
    def edit_tournament(id):
        """Edit a tournament"""
        tournament = Tournament.query.get_or_404(id)

        if request.method == 'GET':
            return render_template('tournament/edit_tournament.html', tournament=tournament)
        elif request.method == 'POST':
            tournament.name = request.form.get('name')
            tournament.sport_type = request.form.get('sport_type')
            tournament.format = request.form.get('format')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            try:
                tournament.start_date = datetime.strptime(start_date, '%Y-%m-%d')
                tournament.end_date = datetime.strptime(end_date, '%Y-%m-%d')

                if tournament.end_date < tournament.start_date:
                    flash("ERROR: End date must be after start date")
                    return redirect('/tournaments/edit')

                db.session.commit()
                flash("Tournament updated successfully!")
                return redirect(f'/tournaments')
            except ValueError:
                flash("ERROR: Invalid date format. Please use YYYY-MM-DD.")
                return redirect('/tournaments/edit')

    @app.route('/tournaments/<id>/delete', methods=['POST'], endpoint='delete_tournament')
    @login_required
    def delete_tournament(id):
        """Delete a tournament"""
        tournament = Tournament.query.get_or_404(id)
        db.session.delete(tournament)
        db.session.commit()
        flash("Tournament deleted successfully!")
        return redirect('/tournaments')

    @app.route('/tournaments/<id>/register', methods=['POST', 'GET'], endpoint='register_team')
    @login_required
    def register_team(id):
        """Register a new team in a tournament"""
        if request.method == 'GET':
            tournament = Tournament.query.get_or_404(id)
            return render_template('tournament/register_team.html', tournament=tournament)
        elif request.method == 'POST':
            tournament = Tournament.query.get_or_404(id)
            team_name = request.form.get('name')  
            contact_info = request.form.get('contact_info')
            group_name = request.form.get('group_name')
            members = request.form.get('members')

            new_team = Team(
                name=team_name,
                tournament_id=tournament.id,
                contact_info=contact_info,
                group_name=group_name,
                members=members
            )
            db.session.add(new_team)
            db.session.commit()
            flash("Team registered successfully!")
            return redirect(f'/tournaments/{id}')

    @app.route('/tournaments/<id>/teams/add-existing', methods=['GET', 'POST'], endpoint='add_existing_team')
    @login_required
    def add_existing_team(id):
        """Add an existing team from another tournament"""
        tournament = Tournament.query.get_or_404(id)

        if tournament.creator_id != current_user.id:
            flash('You are not allowed to add teams to this tournament.')
            return redirect(f'/tournaments/{id}')

        available_teams = Team.query.join(Tournament).filter(
            Tournament.creator_id == current_user.id,
            Team.tournament_id != tournament.id
        ).order_by(Team.name.asc()).all()

        if request.method == 'GET':
            return render_template(
                'tournament/add_existing_team.html',
                tournament=tournament,
                available_teams=available_teams
            )

        source_team_id = request.form.get('source_team_id')
        source_team = Team.query.join(Tournament).filter(
            Team.id == source_team_id,
            Tournament.creator_id == current_user.id
        ).first()

        if not source_team:
            flash('Selected team is invalid.')
            return redirect(f'/tournaments/{id}/teams/add-existing')

        if source_team.tournament_id == tournament.id:
            flash('This team is already in the selected tournament.')
            return redirect(f'/tournaments/{id}/teams/add-existing')

        existing_name = Team.query.filter_by(
            tournament_id=tournament.id,
            name=source_team.name
        ).first()
        if existing_name:
            flash('A team with the same name already exists in this tournament.')
            return redirect(f'/tournaments/{id}/teams/add-existing')

        cloned_team = Team(
            name=source_team.name,
            tournament_id=tournament.id,
            contact_info=source_team.contact_info,
            group_name=source_team.group_name,
            members=source_team.members
        )
        db.session.add(cloned_team)
        db.session.commit()

        flash('Existing team added to tournament successfully!')
        return redirect(f'/tournaments/{id}')

    @app.route('/tournaments/<id>/matches/generate', methods=['POST'], endpoint='generate_matches')
    @login_required
    def generate_matches(id):
        """Generate matches for a tournament"""
        tournament = Tournament.query.get_or_404(id)

        if tournament.creator_id != current_user.id:
            flash('You are not allowed to generate matches for this tournament.')
            return redirect(f'/tournaments/{id}')

        if Team.query.filter_by(tournament_id=tournament.id).count() < 2:
            flash('Need at least 2 teams to generate matches.')
            return redirect(f'/tournaments/{id}')

        existing_matches = Match.query.filter_by(tournament_id=tournament.id).all()
        if existing_matches:
            has_played_match = any(
                match.status == 'completed' or match.result is not None
                for match in existing_matches
            )

            if has_played_match:
                flash('Cannot regenerate because some matches already have results.')
                return redirect(f'/tournaments/{id}')

            for match in existing_matches:
                db.session.delete(match)
            db.session.flush()

        format_name = (tournament.format or '').strip().lower()
        created_count = 0

        if format_name == 'round robin':
            created_count = generate_round_robin_matches(tournament)
        elif format_name == 'knockout':
            created_count = generate_knockout_matches(tournament)
        else:
            flash('This format is not supported yet. Please use Round Robin or Knockout.')
            return redirect(f'/tournaments/{id}')

        db.session.commit()
        if existing_matches:
            flash(f'Successfully refreshed schedule with {created_count} matches.')
        else:
            flash(f'Successfully generated {created_count} matches.')
        return redirect(f'/matches?tournament_id={tournament.id}')
