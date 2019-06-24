# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the pythOnBoarding app
"""
import os
from re import search

from slackclient import SlackClient

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistent memory store.
authed_team = None


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
        self.verification = 'kRrADCUP86toKl9XhiIILJP8'  # kRrADCUP86toKl9XhiIILJP8

        # NOTE: Python-slack requires a client connection to generate
        # an OAuth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = SlackClient('')

        self.bot_id = ''

    def auth(self, code):
        auth_response = self.client.api_call(
            "oauth.access",
            client_id=self.oauth["client_id"],
            client_secret=self.oauth["client_secret"],
            code=code
        )
        print(auth_response)
        authed_team = {"bot_token":
                       auth_response["bot"]["bot_access_token"],
                       'bot_id': auth_response['bot']['bot_user_id']}
        
        self.client = SlackClient(authed_team['bot_token'])
        self.bot_id = authed_team['bot_id']

    def onboarding_message(self, command, result, event):
        """
        Create and send an onboarding welcome message to users's command.

        Parameters
        ----------
        user_id : str
            id of the Slack user associated with the incoming event
        """
        # default_response = "I don't understand what you are saying, Try *help*"

        response = None

        print('command', command)

        if 'escalate' in command:
            response = 'Contact info is:\n' +\
                'Customer: %s\n' % (result.owner_name) +\
                'Telephone number: %s' % (result.tel)

        print(response)

        default_response = "Unreconized command. Please try again."

        self.client.api_call("chat.postMessage",
                             channel=event['channel'],
                             icon_emoji=self.emoji,
                             text=response or default_response
                             )

    def parse_input(self, text):
        metion_regex = "^<@(|[WU].+?)>(.*)"
        match = search(metion_regex, text)
        print(match.groups())
        return match.groups() if match else (None, None)

    def default_answer(self, slack_event):
        response = None
        if 'hello' in slack_event['text']:
            response = 'Hi <@' + slack_event['user'] + '>! What can I do for you?'
        else:
            response = 'I don\'t understand'

        self.client.api_call('chat.postMessage',
                             channel=slack_event['channel'],
                             icon_emoji=self.emoji,
                             text=response)


if __name__ == "__main__":
    Bot().parse_input('<@UKQ6UPY3G> command params')
