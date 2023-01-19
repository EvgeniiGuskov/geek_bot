from typing import Dict
from telebot.types import Message
from config.telebot.telebot import Telebot

from src.view.message_sender import MessageSender

from src.controller.user_data_collector import UserDataCollector
from src.view.commands_handlers.mustwatch_rating_handler.mustwatch_rating_response import MustwatchRatingResponse


class MustwatchRatingCommandHandler:

    def __init__(self, telebot):
        self.bot = telebot.bot

    async def send_mustwatches_rating(self, message: Message,
                                      rated_watches_dict: Dict[str, float]) -> None:
        bot_response_content = MustwatchRatingResponse.make_bot_message_mustwatches_rating(rated_watches_dict)
        await self.bot.send_message(message.chat.id, bot_response_content)
