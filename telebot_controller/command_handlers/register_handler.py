from telebot.types import Message
from telebot_controller.command_handlers.helpers.user_data_collector import UserDataCollector


class RegisterHandler(UserDataCollector):
    __SUCCESSFUL_REGISTRATION_MESSAGE = "Регистрация прошла успешно!"
    __ALREADY_REGISTERED_MESSAGE = "Вы уже зарегистрированы в этой группе!"

    async def register_command_response(self, message: Message, register_result: bool) -> None:
        if register_result:
            await self.bot.reply_to(message, RegisterHandler.__SUCCESSFUL_REGISTRATION_MESSAGE)
        else:
            await self.bot.reply_to(message, RegisterHandler.__ALREADY_REGISTERED_MESSAGE)
