from telebot.async_telebot import AsyncTeleBot

import asyncio

from telebot_secrets import TelebotSecrets


class Telebot:
    __TOKEN = TelebotSecrets.TOKEN

    def __init__(self):
        self.bot = AsyncTeleBot(TelebotSecrets.TOKEN)

    def poll(self):
        asyncio.run(self.bot.polling())
