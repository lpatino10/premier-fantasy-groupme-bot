from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from home.functions import base_url
from home.functions import choose_response
from home.functions import get_total_score
import json
import requests

post_url = '/bots/post'
bot_id = 'cb7fdea6c4bbcb0fea5ef5a5d8'

@csrf_exempt
def index(request):
    if request.method == 'POST':
        message_json = json.loads(request.body)

        if message_json['sender_type'] == 'user':

            # choose_response() will handle deciding the correct course of action and returning a proper response,
            # which could be none at all
            reply = choose_response(message_json)
            if reply:
                requests.post(base_url + post_url, data = {'bot_id': bot_id, 'text': reply})

    return render(request, 'home/index.html')