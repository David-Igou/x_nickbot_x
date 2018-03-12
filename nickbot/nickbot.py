import os
import time
import re
import requests
from slackclient import SlackClient
from riotwatcher import RiotWatcher
from player import Player

# instantiate with Slack and Riot
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
riot_token = os.environ.get('RIOT_TOKEN')
region = 'na1'
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

playerdict = {} #TODO: Add a player list class or something like that

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "No"

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!s

    if command.startswith("addsummoner"):
        try:
            playerdict[command.split()[1]] = Player(command.split()[1],region,riot_token)
        except(requests.exceptions.HTTPError):
            response = "Player not found"
        if(response == None):
            response = "Player successfully added. " + playerdict[command.split()[1]].summary()

    if command.startswith("summary"):
        if(command.split()[1] in playerdict):
            response = playerdict[command.split()[1]].summary()
        else: response = "Player not found"

    if command.startswith("pull"):
        if(command.split()[1] in playerdict):
            playerdict[command.split()[1]].getLastGames()
            response = "Success? I didn't crash"
        else: response = "Player not found"

    if command.startswith("totaldeaths"):
        if(command.split()[1] in playerdict):
            response = str(playerdict[command.split()[1]].getTotalDeaths())
        else: response = "Player not found"

# Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
