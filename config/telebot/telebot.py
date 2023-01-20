import asyncio
from telebot.async_telebot import AsyncTeleBot

from config.telebot.bot_config import TelebotConfig


class Telebot:
    __TOKEN = TelebotConfig.TOKEN

    def __init__(self):
        self.bot = AsyncTeleBot(TelebotConfig.TOKEN)

    def poll(self):
        asyncio.run(self.bot.polling())
