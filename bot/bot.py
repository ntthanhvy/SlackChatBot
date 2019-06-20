# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the pythOnBoarding app
"""
import os

from slackclient import SlackClient

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistent memory store.
authed_teams = {}


class Bot(object):
    """ Instantiates a Bot object to handle Slack onboarding interactions."""

    def __init__(self):
        super(Bot, self).__init__()
        self.name = "pythonboardingBot"
        self.emoji = ":robot_face:"
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": '452524853910.669936981783',
                      "client_secret": '81d290783bd28befb071755e0021612c',
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = 'kRrADCUP86toKl9XhiIILJP8'

        # NOTE: Python-slack requires a client connection to generate
        # an OAuth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = SlackClient(
            'xoxb-452524853910-670232814118-e7nhibVDmCuKsnMVXWm8nMgi')
        # We'll use this dictionary to store the state of each message object.
        # In a production environment you'll likely want to store this more
        # persistently in  a database.

        self.bot_id = self.client.api_call("auth.test")["user_id"]

    def onboarding_message(self, event):
        """
        Create and send an onboarding welcome message to users's command.

        Parameters
        ----------
        user_id : str
            id of the Slack user associated with the incoming event
        """
        default_response = "I don't understand what you are saying, Try *help*"
        print(self.bot_id)
        response = None
        if 'hello' in event['text']:
            response = "Hi <@" + event['user'] + '>! What can I do for you?'

        if 'subtype' in event:
            response = self.handle_subtype(event)

        else:
            data = self.handle_input(event['text'])
            if data:
                response = "Error noted."
                self.client.api_call("chat.postMessage",
                            channel=event['channel'],
                            icon_emoji=self.emoji,
                            text=response or default_response
                            )
                return data
            

        self.client.api_call("chat.postMessage",
                            channel=event['channel'],
                            icon_emoji=self.emoji,
                            text=response or default_response
                            )
        
        return None
        
    def handle_subtype(self, event):
        if event['subtype'] == 'channel_join':
            id = event['user']
            if id == self.bot_id:
                message = "Greeting everyone! I am <@" + self.bot_id + ">."
                return message
            else:
                return "Hi <@" + id + ">. Great to have you here with us."
    
    def handle_input(self, text):
        inp = text.split(' ', 1)
        
        if inp[0].startswith('error'):
            error = inp[1].strip().split(' ', 1)
            return error

        return None

    def parse_input(self, text):
        inp = text.split(' ', 1)
        if 'server' in inp[0]:
            infos = inp[1].split(',')
            data = {
                'server_name': infos[0].strip(),
                'ram': int(infos[1].strip()),
                'cpu': int(infos[2].strip()),
                'owner': [name for name in infos[-1].strip().split()]
            }
            return data

    def result(self, data, event):
        message = "Query successful with data" + str(data)
        self.client.api_call("chat.postMessage",
                            channel=event['channel'],
                            icon_emoji=self.emoji,
                            text=message
                            )
