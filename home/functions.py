#def get_current_standings():

def get_total_score(name):
    standings = requests.get('https://fantasy.premierleague.com/drf/leagues-classic-standings/508077').json()
    score = 0
    for player in standings['standings']['results']:
        if player['player_name'] == name:
            score = player['total']
    return score

#def get_current_week_score(name):

#def get_current_position(name):