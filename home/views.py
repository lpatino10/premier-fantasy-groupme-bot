from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from home.functions import get_total_score
import json
import requests

@csrf_exempt
def index(request):
    if request.method == 'POST':
        message_json = json.loads(request.body)
        message_text = message_json['text']

        if ('blart' in message_text.lower()) and (message_json['sender_type'] == 'user'):
            player_name =  message_json['name']

            for attachment in message_json['attachments']:
                if attachment['type'] == 'mention':
                    player_name = attachment['user_ids'][0]
                    break
            
            score = get_total_score(player_name)
            return_message = 'Your current fantasy score is: {}'.format(score)
            requests.post('https://api.groupme.com/v3/bots/post', data = {'bot_id': 'cb7fdea6c4bbcb0fea5ef5a5d8', 'text': return_message})
    return render(request, 'home/index.html')