# Constants configuration

# Scoring system for tournament standings
STANDINGS_POINTS = {
    'WIN': 3,
    'DRAW': 1,
    'LOSS': 0
}

# Tournament formats
TOURNAMENT_FORMATS = [
    'Round Robin',
    'Knockout',
    'Swiss',
    'Group Stage+Knockout'
]

# Match statuses
MATCH_STATUSES = [
    'scheduled',
    'ongoing',
    'completed',
    'cancelled'
]

# Database field length limits
STRING_LIMITS = {
    'USERNAME': 100,
    'EMAIL': 255,
    'TOURNAMENT_NAME': 200,
    'TEAM_NAME': 200,
    'SPORT_TYPE': 50,
    'TOURNAMENT_FORMAT': 50,
    'CONTACT_INFO': 255,
    'GROUP_NAME': 50,
    'MATCH_STATUS': 20,
    'VENUE': 255,
    'ROUND': 50,
}
