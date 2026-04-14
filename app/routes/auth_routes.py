from flask import render_template, request, redirect
from app.models import db, User
from flask_login import login_user, logout_user


def register_auth_routes(app, bcrypt):
    """Register authentication routes to the Flask app"""

    @app.route('/register', methods=['GET', 'POST'], endpoint='register')
    def register():
        """Register a new user"""
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return "User already exists"

            email = request.form.get('email') or f'{username}@example.com'
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            return redirect('/')

    @app.route('/login', methods=['GET', 'POST'], endpoint='login')
    def login():
        """Login a user"""
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                return redirect('/')
            else:
                return "Invalid username or password"

    @app.route('/logout', endpoint='logout')
    def logout():
        """Logout a user"""
        logout_user()
        from flask import flash
        flash("Successfully logged out")
        return redirect('/')
