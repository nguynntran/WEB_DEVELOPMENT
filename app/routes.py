from flask import Blueprint, render_template, request, jsonify
from app.models import db, Tournament, Team, Match

def register_routes(app, db ):
    @app.route("/")
    def home():
        return render_template('home.html')
    
    @app.route('/tournaments')
    def tournaments():
        return render_template('tournaments.html')

    @app.route('/teams')
    def teams():
        return render_template('teams.html')

    @app.route('/matches')
    def matches():
        return render_template('matches.html')

    @app.route('/standings')
    def standings():
        return render_template('standings.html')