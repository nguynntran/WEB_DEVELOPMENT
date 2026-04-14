from flask import render_template


def register_routes(app, db, bcrypt):
    """Register all routes to the Flask app"""
    
    # Home route
    @app.route("/", endpoint='home')
    def home():
        return render_template('home.html')
    
    # Import and register tournament routes
    from .tournament_routes import register_tournament_routes
    register_tournament_routes(app, db)
    
    # Import and register team routes
    from .team_routes import register_team_routes
    register_team_routes(app, db)
    
    # Import and register match routes
    from .match_routes import register_match_routes
    register_match_routes(app, db)
    
    # Import and register standing routes
    from .standing_routes import register_standing_routes
    register_standing_routes(app, db)
    
    # Import and register auth routes
    from .auth_routes import register_auth_routes
    register_auth_routes(app, bcrypt)

