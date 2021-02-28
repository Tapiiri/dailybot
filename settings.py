import os
import datetime
from dotenv import load_dotenv
load_dotenv()


# Variables set on environment when possible

# Required
TOKEN = os.environ.get("TOKEN", "")
NAME = os.environ.get("NAME", "")
HOUR = int(os.environ.get("HOUR", 10))
MINUTE = int(os.environ.get("MINUTE", 00))
TIMEZONE = int(os.environ.get("TIMEZONE", 00))
DAILY_TIME = datetime.time(hour=HOUR-TIMEZONE, minute=MINUTE)
DAYS =  tuple([int(d) for d in os.environ.get("DAYS", "0").split(',')])

# File locations
START_FILE = "app/msg/start.md"
DAILY_FILE = "app/msg/daily.md"
EXAMPLE_FILE = "app/msg/example.md"
ERROR_FILE = "app/msg/error.md"

CHAT_IDS = os.environ.get("CHAT_IDS", "").replace(" ", "").split(",")

# Port and link is given by Heroku/ngrok
PORT = os.environ.get("PORT", None)
LINK = os.environ.get("LINK", None)
