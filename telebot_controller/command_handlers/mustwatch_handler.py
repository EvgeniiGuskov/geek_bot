from telebot_controller.command_handlers.helpers.user_data_collector import UserDataCollector
from telebot_controller.command_handlers.helpers.buttons import Button


class MustwatchHandler(UserDataCollector):
    __USER_IS_NOT_REGISTERED_MESSAGE = "Пользователь не зарегистрирован!"
    __USER_IS_NOT_REGISTERED_MESSAGE = "Чтобы пользоваться ботом, вам нужно зарегистрироваться!"
    __ADD_OR_DELETE_MESSAGE = "Что вы хотите сделать?"
    __CHOOSE_USER_TO_ADD_MESSAGE = "Кому добавить маствотч?"
    __CHOOSE_USER_TO_DELETE_MESSAGE = "Кому удалить маствотч?"
    __CHOOSE_ONE_USER_MESSAGE = "Выберите пользователя"
    __ADD_OR_CHOOSE_MUSTWATCH_MESSAGE = "Список маствотчей для добавления"
    __CHOOSE_MUSTWATCH_TO_DELETE_MESSAGE = "Список маствотчей для удаления"
    __SEND_ITEM_TITLE_MESSAGE = "Отправьте название маствотча:"
    __CHANGE_REQUEST_MESSAGE = "Хотите что-то поменять?"
    __END_MESSAGE = "Сделано!"

    async def __edit_message_to_choose_user_buttons(self, call, bot_message):
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_choose_user_add_item
        )

    async def __edit_message_to_choose_specific_user_buttons(self, call, bot_message, user_dict):
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_choose_specific_user,
            user_dict
        )

    async def __edit_message_to_add_or_choose_title(self, call, bot_message):
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_choose_title
        )

    async def __edit_message_to_choose_title(self, call, bot_message):
        await self.edit_message_text_and_delete_buttons(
            call,
            bot_message
        )

    async def __edit_message_to_confirm_request(self, chat_id, message_id, bot_message):
        await self.edit_message_text_and_buttons(
            chat_id,
            message_id,
            bot_message,
            self.markup_confirm_user_request
        )

    async def __edit_message_to_choose_step(self, call, bot_message):
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_choose_step
        )

    async def __edit_message_to_add_or_delete(self, call, bot_message):
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_add_or_delete_item
        )

    async def __edit_message_to_end(self, call, bot_message):
        await self.edit_message_text_and_delete_buttons(call, bot_message)

    async def start_conversation_with_user(self, message, register_state, chat_id, user_id):
        if not register_state:
            await self.bot.reply_to(message,
                                    MustwatchHandler.__USER_IS_NOT_REGISTERED_MESSAGE)
        else:
            msg = await self.bot.reply_to(message,
                                          MustwatchHandler.__ADD_OR_DELETE_MESSAGE,
                                          reply_markup=self.markup_add_or_delete_item())
            return chat_id, user_id, msg.id

    async def edit_add_or_delete_response_to_choose_user(self, call, add_or_delete):
        if add_or_delete:
            await self.__edit_message_to_choose_user_buttons(call, MustwatchHandler.__CHOOSE_USER_TO_ADD_MESSAGE)
        else:
            await self.__edit_message_to_choose_title(call, MustwatchHandler.__CHOOSE_MUSTWATCH_TO_DELETE_MESSAGE)

    async def edit_choose_user_response_to_choose_specific_user(self, call, user_dict):
        await self.__edit_message_to_choose_specific_user_buttons(call,
                                                                  MustwatchHandler.__CHOOSE_ONE_USER_MESSAGE,
                                                                  user_dict
                                                                  )

    async def edit_choose_user_response_to_choose_title(self, call):
        await self.__edit_message_to_add_or_choose_title(call, MustwatchHandler.__ADD_OR_CHOOSE_MUSTWATCH_MESSAGE)

    async def edit_add_or_choose_title_to_send_title(self, call):
        await self.edit_message_text_and_delete_buttons(call, MustwatchHandler.__SEND_ITEM_TITLE_MESSAGE)

    async def edit_send_title_response_to_confirm_request(self, chat_id, message_id, bot_message):
        await self.__edit_message_to_confirm_request(chat_id, message_id, bot_message)

    def __get_add_or_delete_word(self, add_or_delete):
        if add_or_delete:
            return Button.ADD_BUTTON[0]
        else:
            return Button.DELETE_BUTTON[0]

    async def __get_chosen_user_word(self, message, chosen_user):
        if chosen_user == Button.ME_BUTTON_CALLBACK:
            return Button.ME_BUTTON[0].lower()
        elif chosen_user == Button.ALL_BUTTON_CALLBACK:
            return Button.ALL_BUTTON[0].lower()
        else:
            return "пользователю " + await self.get_user_fullname(message.chat.id, int(chosen_user))

    async def make_bot_message_from_user_request_values(self, message, add_or_delete, title, chosen_user):
        add_or_delete_word = self.__get_add_or_delete_word(add_or_delete)
        title_word = title
        chosen_user_word = await self.__get_chosen_user_word(message, chosen_user)
        return add_or_delete_word + " " + chosen_user_word + " " + '"' + title_word + '"?'

    async def edit_confirm_request_response_to_conversation_end(self, call):
        if call.data == Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK:
            await self.__edit_message_to_choose_step(call, MustwatchHandler.__CHANGE_REQUEST_MESSAGE)
        else:
            await self.__edit_message_to_end(call, MustwatchHandler.__END_MESSAGE)

    async def edit_choose_step_message_response_to_chosen_step(self, call):
        if call.data == self.START_OVER_BUTTON_CALLBACK:
            await self.__edit_message_to_add_or_delete(call, MustwatchHandler.__ADD_OR_DELETE_MESSAGE)
        else:
            await self.edit_choose_user_response_to_choose_title(call)
