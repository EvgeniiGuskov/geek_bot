from telebot.async_telebot import AsyncTeleBot

import asyncio

from telebots_potion_store.robots.register_robot import RegisterRobot
from telebots_potion_store.robots.mustwatch_robots.mustwatch_robot import MustwatchRobot
from telebot_secrets import TelebotSecrets


class Telebot(RegisterRobot, MustwatchRobot):
    __TOKEN = TelebotSecrets.TOKEN

    def __init__(self):
        self.bot = AsyncTeleBot(TelebotSecrets.TOKEN)

    def poll(self):
        asyncio.run(self.bot.polling())