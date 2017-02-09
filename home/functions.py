import requests

username_dict = {'poonslayer': 'McCoy Patino'}

#def get_current_standings():

def get_total_score(name):
    name = convert_name(name)
    standings = requests.get('https://fantasy.premierleague.com/drf/leagues-classic-standings/508077').json()
    score = 0
    for player in standings['standings']['results']:
        if player['player_name'] == name:
            score = player['total']
    return score

#def get_current_week_score(name):

#def get_current_position(name):

def convert_name(name):
    new_name = name
    if name in username_dict:
        new_name = username_dict[name]
    return new_name