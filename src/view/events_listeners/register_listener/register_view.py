from telebot.types import Message

from src.view.events_listeners.register_listener.register_response import RegisterResponse


class RegisterListener:

    def __init__(self, telebot):
        self.bot = telebot.bot

    async def register_command_response(self,
                                        message: Message,
                                        is_user_registered: bool) -> None:
        bot_response_content = RegisterResponse.get_response_to_register(is_user_registered)
        await self.bot.reply_to(message, bot_response_content)
