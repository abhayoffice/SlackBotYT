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

message_counts = {}
# client.chat_postMessage(channel="#test", text = "Hello World!")

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    # client.chat_postMessage(channel= channel_id, text=text)

    if BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id]+=1
        else:
            message_counts[user_id]=1
        # client.chat_postMessage(channel= channel_id, text=text)


@app.route("/message_count", methods=['POST'])
def message_count():
    data = request.form
    print(data)
    user_id = data.get('user_id')
    username = data.get('user_name')
    channel_id = data.get('channel_id')
    message_cnt = message_counts.get(user_id,0)
    # if user_id in message_counts:
    #     client.chat_postMessage(channel=channel_id, text = username)
    client.chat_postMessage(channel=channel_id, text = f"The message count is : {message_cnt}")
    return Response(), 200


if __name__ == "__main__":
    # schedule_messages(SCHEDULED_MESSAGES)
    # ids = list_scheduled_messages('C01BXQNT598')
    # delete_scheduled_messages(ids, 'C01BXQNT598')
    app.run(debug=True)