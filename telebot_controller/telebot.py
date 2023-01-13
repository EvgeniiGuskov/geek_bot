from telebot.async_telebot import AsyncTeleBot

import asyncio

from telebot_controller.command_handlers.register_handler import RegisterHandler
from telebot_controller.command_handlers.mustwatch_handler import MustwatchHandler
from telebot_controller.command_handlers.mustwatch_rating_handler import MustwatchRatingHandler
from telebot_secrets import TelebotSecrets


class Telebot(RegisterHandler, MustwatchHandler, MustwatchRatingHandler):
    __TOKEN = TelebotSecrets.TOKEN

    def __init__(self):
        self.bot = AsyncTeleBot(TelebotSecrets.TOKEN)

    def poll(self):
        asyncio.run(self.bot.polling())
