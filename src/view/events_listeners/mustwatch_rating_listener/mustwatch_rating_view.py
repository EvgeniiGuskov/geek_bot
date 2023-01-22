from typing import Dict

from telebot.types import Message

from src.view.events_listeners.mustwatch_rating_listener.mustwatch_rating_response import MustwatchRatingResponse


class MustwatchRatingView:

    def __init__(self, telebot):
        self.bot = telebot.bot

    async def send_mustwatches_rating(self, message: Message,
                                      rated_watches_dict: Dict[str, float]) -> None:
        bot_response_content = MustwatchRatingResponse.make_bot_message_mustwatches_rating(rated_watches_dict)
        await self.bot.send_message(message.chat.id, bot_response_content)
