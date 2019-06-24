# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
from bot.bot import Bot
from flask import Flask, request, make_response, render_template
from datetime import datetime

from db.connect_db import Session
from db.import_data import new_server, add_contact_info, add_escalate
from db.get_data import get_contact_info, get_server_info

pyBot = Bot()
slack = pyBot.client

app = Flask(__name__)


session = Session()


def handle_command(cmd, params):

    if cmd == 'escalate':
        customer, reason = params.split(' ', 1)
        time = datetime.today().replace(microsecond=0)
        data = {
            'time': time,
            'customer': customer,
            'type': reason
        }
        result = add_escalate(session, data)
        contact_info = get_contact_info(session, result)
        return contact_info[0]
    
    return None


def _event_handler(slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.
    Parameters
    ----------
    slack_event : dict
        JSON response from a Slack reaction event
    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error
    """
    event_type = slack_event['type']

    if not 'subtype' in slack_event and 'app_mention' in event_type:
        user_id, text = pyBot.parse_input(slack_event['text'])
        if user_id == pyBot.bot_id:
            if len(text.split()) > 1:
                command, params = text.strip().split(' ', 1)
                result = handle_command(command, params)
                try:
                    session.commit()
                except AttributeError:
                    pass
                pyBot.onboarding_message(command, result, slack_event)
            else:
                pyBot.default_answer(slack_event)
            
            return make_response("Event hanled", 200,)

    elif 'channel_join' in event_type or 'team_join' in event_type:
        # pyBot.welcome(slack_event)
        pass

    # # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/install", methods=["GET"])
def pre_install():
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    client_id = pyBot.oauth["client_id"]
    scope = pyBot.oauth["scope"]
    # Our template is using the Jinja templating language to dynamically pass
    # our client id and scope
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
    code_args = request.args.get('code')
    pyBot.auth(code_args)
    return make_response("Authentication Success", 200)


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """

    slack_event=request.get_json()
    # ============= Slack URL Verification ============ #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    #       For more info: https://api.slack.com/events/url_verification
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })

    if pyBot.verification != slack_event['token']:
        message="Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # ====== Process Incoming Events from Slack ======= #
    # If the incoming request is an Event we've subscribed to
    if 'event' in slack_event:
        print(slack_event)
        slack_event=slack_event['event']
        return _event_handler(slack_event)


    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True)
