from telebots_potion_store.robots.mustwatch_robots.manage_mustwatch_robot import ManageMustwatchRobot
from telebots_potion_store.robots.nanobots.inline_markup_nanobot import InlineMarkupNanobot


class UserDataCollector(ManageMustwatchRobot):
    def __get_user_data_from_call(self, call):
        chat_id = str(call.message.chat.id)
        user_id = str(call.from_user.id)
        message_id = str(call.message.id)
        return chat_id, user_id, message_id

    def __get_user_choice_from_call(self, call, true_button, false_button):
        if call.data in (true_button[1], false_button[1]):
            if call.data == true_button[1]:
                add_or_delete = True
            else:
                add_or_delete = False
            return *self.__get_user_data_from_call(call), add_or_delete

    def get_user_choice_from_add_or_delete_call(self, call):
        return self.__get_user_choice_from_call(call, InlineMarkupNanobot.ADD_BUTTON, InlineMarkupNanobot.DELETE_BUTTON)

    def get_user_data_from_to_me_call(self, call):
        if call.data == self.ME_BUTTON[1]:
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            return chat_id, user_id
