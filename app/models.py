from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Models

# User model for authentication
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



# Tournament Model
class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),  nullable = False)
    sport_type = db.Column(db.String(50), nullable = False)
    format = db.Column(db.String(50), nullable = False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    end_date = db.Column(db.DateTime, nullable = False)
    creator_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teams = db.relationship('Team', backref='tournament', lazy=True)
    matches = db.relationship('Match', backref='tournament', lazy=True)
    standings = db.relationship('Standing', backref='tournament', lazy=True)

    def __repr__(self):
        return f'<Tournament {self.name}>'

# Team model
class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    contact_info = db.Column(db.String(255))
    group_name = db.Column(db.String(50))
    members = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    home_matches = db.relationship('Match', foreign_keys='Match.team1_id', backref='team1', lazy='dynamic')
    away_matches = db.relationship('Match', foreign_keys='Match.team2_id', backref='team2', lazy='dynamic')
    standings = db.relationship('Standing', backref='team', lazy='dynamic')
    
    def __repr__(self):
        return f'<Team {self.name}>'

# Match model
class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime)
    venue = db.Column(db.String(255))
    round = db.Column(db.String(50))
    status = db.Column(db.String(20), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    result = db.relationship('Result', backref='match', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Match {self.id}: Team{self.team1_id} vs Team{self.team2_id}>'

# Result model
class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False, unique=True)
    team1_score = db.Column(db.Integer, nullable=False)
    team2_score = db.Column(db.Integer, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  
    
    winner = db.relationship('Team', foreign_keys=[winner_id])
    submitter = db.relationship('User', foreign_keys=[submitted_by])
    
    def __repr__(self):
        return f'<Result Match{self.match_id}: {self.team1_score}-{self.team2_score}>'
    
# Standing Model
class Standing(db.Model):
    __tablename__ = 'standings'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    points = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Standing Team{self.team_id}: {self.points} pts>'