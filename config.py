import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('TOKEN')
ELEVENLABS_TOKEN = os.getenv('ELEVENLABS_TOKEN')
