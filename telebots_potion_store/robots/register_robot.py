class RegisterRobot():
    __SUCCESSFUL_REGISTRATION_MESSAGE = "Регистрация прошла успешно!"
    __ALREADY_REGISTERED_MESSAGE = "Вы уже зарегистрированы в этой группе!"

    def get_user_data(self, message):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        username = message.from_user.username
        return chat_id, user_id, username

    async def register_command_response(self, message, register_result):
        if register_result:
            await self.bot.reply_to(message, RegisterRobot.__SUCCESSFUL_REGISTRATION_MESSAGE)
        else:
            await self.bot.reply_to(message, RegisterRobot.__ALREADY_REGISTERED_MESSAGE)
