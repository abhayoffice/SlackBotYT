import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter


load_dotenv()

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET_'], '/myslack/events', app)


client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")["user_id"]

# client.chat_postMessage(channel="#test", text = "Hello World!")

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        client.chat_postMessage(channel= channel_id, text=text)




if __name__ == "__main__":
    # schedule_messages(SCHEDULED_MESSAGES)
    # ids = list_scheduled_messages('C01BXQNT598')
    # delete_scheduled_messages(ids, 'C01BXQNT598')
    app.run(debug=True)