from telebot.types import Message
from config.telebot.telebot import Telebot

from src.view.commands_handlers.register_handler.register_response import RegisterResponse
from src.view.message_sender import MessageSender


class RegisterCommandHandler:

    def __init__(self, telebot):
        self.bot = telebot.bot

    async def register_command_response(self,
                                        message: Message,
                                        is_user_registered: bool) -> None:
        bot_response_content = RegisterResponse.get_response_to_register(is_user_registered)
        await self.bot.reply_to(message, bot_response_content)
