import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter


load_dotenv()

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET_'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN_'])

