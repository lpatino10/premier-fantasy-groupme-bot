import requests
import logging
from watson_developer_cloud import NaturalLanguageClassifierV1

logger = logging.getLogger(__name__)

fantasy_url = 'https://fantasy.premierleague.com/drf/leagues-classic-standings/508077'
base_url = 'https://api.groupme.com/v3'
group_url = '/groups/'
group_id = '17077713'
token = '?token=jU44oU4exOUdK3Fr7pkvbnP3Z7NlVilNNQY5dqkR'

classifier_id = 'f5b42fx173-nlc-3572'
confidence_limit = 0.98

not_yet_functioning_reponse = "I can't help you with this yet, but I should be able to soon!"
username_dict = {'poonslayer': 'McCoy Patino',
  'Craig Casto': 'Craig C'}

def get_current_standings():
    return not_yet_functioning_reponse

def get_total_score(name):
    name = convert_name(name)
    standings = requests.get(fantasy_url).json()
    score = 0
    for player in standings['standings']['results']:
        if player['player_name'] == name:
            score = player['total']
    return score

def get_current_week_score(name):
    return not_yet_functioning_reponse

def get_current_position(name):
    return not_yet_functioning_reponse

def convert_name(name):
    new_name = name
    if name in username_dict:
        new_name = username_dict[name]
    return new_name

def get_mentioned_name(user_id):
    name = ''
    group_info = requests.get(base_url + group_url + group_id + token).json()
    print(group_info)
    for member in group_info['response']['members']:
        if member['user_id'] == user_id:
            name = member['nickname']
    return convert_name(name)

def get_message_subject(message_json):
    player_name =  message_json['name']
    for attachment in message_json['attachments']:
        if attachment['type'] == 'mentions':
            user_id = attachment['user_ids'][0]
            player_name = get_mentioned_name(user_id)
            break
    player_name = convert_name(player_name)
    return player_name

def choose_response(message_json):
    response = ''
    message_text = message_json['text']

    natural_language_classifier = NaturalLanguageClassifierV1(
        username='6330ae18-60bc-4dfe-8c6d-3f86a7394b56',
        password='MHlzYl0uGbHT')

    classification_response = natural_language_classifier.classify(classifier_id, message_text)

    # logging to see how the classifier's working
    print('Input: {}'.format(message_text))
    for c in classification_response['classes']:
        print('Class: {}  Confidence: {}'.format(c['class_name'], c['confidence']))
    print('')

    top_class = classification_response['classes'][0]
    if top_class['confidence'] < confidence_limit:
        return response

    name = get_message_subject(message_json)
    print('Subject: {}'.format(name))

    top_class_name = top_class['class_name']
    if top_class_name == 'standings':
        response = get_current_standings()
    elif top_class_name == 'total':
        response = get_total_score(name)
    elif top_class_name == 'week':
        response = get_current_week_score(name)
    elif top_class_name == 'position':
        response = get_current_position(name)

    return response