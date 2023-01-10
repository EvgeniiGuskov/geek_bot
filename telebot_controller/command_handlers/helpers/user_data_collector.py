from telebot_controller.command_handlers.helpers.message_editor import MessageEditor
from telebot_controller.command_handlers.helpers.buttons import Button


class UserDataCollector(MessageEditor):

    def __get_chat_id_from_call(self, call):
        return call.message.chat.id

    def __get_user_id_from_call(self, call):
        return call.from_user.id

    def get_user_data_from_message(self, message):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        return chat_id, user_id

    async def get_user_fullname(self, chat_id, user_id):
        chat_member = await self.bot.get_chat_member(chat_id, user_id)
        return chat_member.user.full_name

    def get_user_data_from_call(self, call):
        chat_id = str(self.__get_chat_id_from_call(call))
        user_id = str(self.__get_user_id_from_call(call))
        return chat_id, user_id

    def get_user_data_and_message_id_from_call(self, call):
        message_id = str(call.message.id)
        return *self.get_user_data_from_call(call), message_id

    def get_user_choice_from_call(self, call):
        return *self.get_user_data_from_call(call), call.data

    def get_specific_user_choice_from_call(self, call):
        return *self.get_user_data_from_call(call), call.data.lstrip(
            Button.CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK
        )

    async def convert_telegram_user_id_to_full_name(self, call, user_dict):
        chat_id = str(self.__get_chat_id_from_call(call))
        for key in user_dict:
            user_dict[key] = await self.get_user_fullname(chat_id, int(user_dict[key]))
        return user_dict
