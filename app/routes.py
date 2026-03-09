from flask import Blueprint, render_template, request, redirect, flash
from app.models import db, User, Tournament, Team, Match, Standing
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

def register_routes(app, db, bcrypt):
    @app.route("/")
    def home():
        return render_template('home.html')
    
    # Tournament routes
    @app.route('/tournaments') 
    def tournaments():
        all_tournaments = Tournament.query.order_by(Tournament.start_date.desc()).all()
        return render_template('tournament/tournaments.html', tournaments=all_tournaments)

    @app.route('/tournaments/create', methods = ['GET', 'POST'])
    @login_required
    def create_tournament():
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

            
    
    @app.route('/tournaments/<id>')
    @login_required
    def tournament_detail(id):
        pass

    @app.route('/tournaments/<id>/edit', methods = ['GET', 'POST'])
    @login_required
    def edit_tournament(id):
        pass

    @app.route('/tournaments/<id>/delete', methods = ['POST'])
    @login_required
    def delete_tournament(id):
        pass

# Team routes
    @app.route('/teams')
    def teams():
        return render_template('teams.html')

# Match routes
    @app.route('/matches')
    def matches():
        return render_template('matches.html')

# Standings routes
    @app.route('/standings')
    def standings():
        return render_template('standings.html')

# Authentication routes
    @app.route('/register', methods = ['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return "User already exists"

            # Create new user
            email = request.form.get('email') or f'{username}@example.com'
            new_user = User(username=username, email=email)
            new_user.set_password(password)  # Method này sẽ hash password tự động
            db.session.add(new_user)
            db.session.commit()

            return redirect('/')
    @app.route('/login', methods = ['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Find user
            user = User.query.filter_by(username=username).first()
            
            # Check if user exists and password is correct
            if user and user.check_password(password):
                login_user(user)
                return redirect('/')
            else:
                return "Invalid username or password"

            return redirect('/')
        
    @app.route('/logout')
    def logout():
        logout_user()
        return "Sucessfully logged out"
    return redirect('/')