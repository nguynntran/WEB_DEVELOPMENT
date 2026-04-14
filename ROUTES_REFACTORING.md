# Routes Refactoring Summary

## New Structure

The application routes have been reorganized from a monolithic `routes.py` file into a blueprint-based architecture, matching the template folder structure.

### Folder Structure

```
app/
├── routes/
│   ├── __init__.py                 (Home route + blueprint registration)
│   ├── tournament_routes.py         (6 tournament routes + match generation helpers)
│   ├── team_routes.py               (4 team management routes)
│   ├── match_routes.py              (2 match routes + standings recalculation)
│   ├── standing_routes.py           (1 standings route)
│   └── auth_routes.py               (4 authentication routes)
├── models.py                        (Database models)
├── static/                          (CSS files)
├── templates/                       (HTML templates)
└── __init__.py                      (App factory)
```

## Routes Organization

### Tournament Routes (`tournament_routes.py`)
- `GET/POST /tournaments` - List and filter tournaments
- `GET/POST /tournaments/create` - Create new tournament
- `GET /tournaments/<id>` - View tournament details
- `GET/POST /tournaments/<id>/edit` - Edit tournament
- `POST /tournaments/<id>/delete` - Delete tournament
- `GET/POST /tournaments/<id>/register` - Register new team
- `GET/POST /tournaments/<id>/teams/add-existing` - Add existing team
- `POST /tournaments/<id>/matches/generate` - Generate matches

**Helper Functions:**
- `generate_round_robin_matches()` - Create round robin schedule
- `generate_knockout_matches()` - Create knockout schedule

### Team Routes (`team_routes.py`)
- `GET /teams` - List all teams (grouped by name)
- `GET /teams/<id>` - View team details
- `GET/POST /teams/<id>/edit` - Edit team
- `POST /teams/<id>/delete` - Delete team

### Match Routes (`match_routes.py`)
- `GET /matches` - List matches with tournament filter
- `GET/POST /matches/<id>/result` - Submit/edit match result

**Helper Functions:**
- `recalculate_standings()` - Calculate standings from match results

### Standing Routes (`standing_routes.py`)
- `GET /standings` - View standings with tournament filter

**Helper Functions:**
- `recalculate_standings_helper()` - Calculate standings (with same logic as match_routes)

### Auth Routes (`auth_routes.py`)
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Home Route (`__init__.py`)
- `GET /` - Home page

## Benefits

1. **Better Organization** - Each feature group has its own file (like templates)
2. **Easier Maintenance** - Smaller, focused files are easier to navigate
3. **Scalability** - Easy to add new features or routes
4. **Code Reusability** - Helper functions are now grouped with related routes
5. **Consistent Structure** - Matches the template folder organization

## URL Prefixes

Each blueprint has a URL prefix:
- `tournament_bp` → `/tournaments`
- `team_bp` → `/teams`
- `match_bp` → `/matches`
- `standing_bp` → `/standings`
- `auth_bp` → no prefix (auth routes are at root)

## Migration Notes

- Old `app/routes.py` backed up as `app/routes.py.backup`
- No functional changes - all routes work exactly the same
- `app/__init__.py` remains unchanged (it calls `register_routes()` as before)
- All imports and functionality preserved
