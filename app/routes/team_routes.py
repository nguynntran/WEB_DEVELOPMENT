from flask import render_template, request, redirect, flash
from app.models import db, Tournament, Team
from flask_login import login_required, current_user
from collections import OrderedDict


def register_team_routes(app, db):
    """Register team routes to the Flask app"""

    @app.route('/teams', endpoint='teams')
    @login_required
    def teams():
        """List all teams created by current user, grouped by name"""
        all_teams = Team.query.join(Tournament).filter(
            Tournament.creator_id == current_user.id
        ).order_by(Team.name.asc(), Tournament.name.asc()).all()

        grouped = OrderedDict()
        for team in all_teams:
            key = team.name.strip().lower()
            if key not in grouped:
                grouped[key] = {
                    'name': team.name,
                    'contact_info': team.contact_info,
                    'group_name': team.group_name,
                    'members': team.members,
                    'tournaments': []
                }

            grouped[key]['tournaments'].append({
                'id': team.tournament.id,
                'name': team.tournament.name,
                'team_id': team.id
            })

        grouped_teams = list(grouped.values())
        return render_template('team/teams.html', grouped_teams=grouped_teams)

    @app.route('/teams/<id>', endpoint='team_detail')
    @login_required
    def team_detail(id):
        """View team details"""
        team = Team.query.get_or_404(id)
        return render_template('team/team_detail.html', team=team)

    @app.route('/teams/<id>/edit', methods=['GET', 'POST'], endpoint='edit_team')
    @login_required
    def edit_team(id):
        """Edit a team"""
        if request.method == 'GET':
            team = Team.query.get_or_404(id)
            return render_template('team/edit_team.html', team=team)
        elif request.method == 'POST':
            team = Team.query.get_or_404(id)
            team.name = request.form.get('name')
            team.contact_info = request.form.get('contact_info')
            team.group_name = request.form.get('group_name')
            team.members = request.form.get('members')

            db.session.commit()
            flash("Team updated successfully!")
            return redirect(f'/teams')

    @app.route('/teams/<id>/delete', methods=['POST'], endpoint='delete_team')
    @login_required
    def delete_team(id):
        """Delete a team"""
        pass
