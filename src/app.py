from flask import Flask, request, Response, send_from_directory
import requests
import json
import os
import re

from dict import REPLIES, DICTIONARY
from utils import parse_reply

app = Flask(__name__)

app.static_folder('public')

# env_variables
# token to verify that this bot is legit
verify_token = os.getenv('VERIFY_TOKEN', None)


# token to send messages through facebook messenger
access_token = os.getenv('ACCESS_TOKEN', None)


@app.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"


@app.route('/webhook', methods=['POST'])
def webhook_action():
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        user_message = entry['messaging'][0]['message']['text']
        user_id = entry['messaging'][0]['sender']['id']
        response = {
            'recipient': {'id': user_id},
            'message': {}
        }
        response['message']['text'] = handle_message(user_id, user_message)
        _ = requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
    return Response(response="EVENT RECEIVED", status=200)


@app.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    user_message = data['entry'][0]['messaging'][0]['message']['text']
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    response = {
        'recipient': {'id': user_id},
        'message': {'text': handle_message(user_id, user_message)}
    }
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


def handle_message(user_id, user_message):
    # DO SOMETHING with the user_message ... ¯\_(ツ)_/¯
    for regex in DICTIONARY:
        if re.search(regex, user_message, re.I):
            temp = DICTIONARY[regex].split('.')
            assert len(temp) == 2, "Cannot have more than two parts of the key of the REPLIES index."
            lang, reply = temp

            return parse_reply(REPLIES[lang][reply], uid=user_id, message=user_message)
    return "Hello "+user_id+", I did not understand your input of: " + user_message


@app.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."


@app.route('/user_agreement', methods=['GET'])
def user_agreement():
    # needed route if you need to make your bot public
    return "You agree that if you use this software [...] happens."


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
