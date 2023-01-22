from os import getenv
import asyncio

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot


class Telebot:

    def __init__(self):
        load_dotenv()
        self.bot = AsyncTeleBot(getenv("TOKEN"))

    def poll(self):
        asyncio.run(self.bot.polling())
