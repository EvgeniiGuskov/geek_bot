from telebot.types import CallbackQuery, Message
from telebot_controller.command_handlers.helpers.user_data_collector import UserDataCollector
from telebot_controller.command_handlers.helpers.message_editor import MessageEditor
from telebot_controller.command_handlers.helpers.buttons import Button


class MustwatchHandler(UserDataCollector, MessageEditor, Button):
    __USER_IS_NOT_REGISTERED_MESSAGE = "Чтобы пользоваться ботом, вам нужно зарегистрироваться!"
    __ADD_OR_DELETE_MESSAGE = "Управление маствотчами:"
    __CHOOSE_USER_TO_ADD_MESSAGE = "Кому добавить маствотч?"
    __CHOOSE_ONE_USER_MESSAGE = "Выберите пользователя:"
    __NO_OTHER_USERS_REGISTERED_MESSAGE = "В этой группе пока никто не зарегистрировался..."
    __ADD_OR_CHOOSE_MUSTWATCH_MESSAGE = "Список маствотчей, которые можно добавить:"
    __NO_MORE_MUSTWATCHES_TO_ADD = "Больше нет маствотчей, которые можно было бы добавить выбранному пользователю(ям)..."
    __CHOOSE_MUSTWATCH_TO_DELETE_MESSAGE = "Выберите маствотч, чтобы полностью удалить его из группы:"
    __NO_MORE_MUSTWATCHES_TO_DELETE_MESSAGE = "Пока никто не добавил маствотчи, чтобы их удалить..."
    __CHOOSE_MUSTWATCH_TO_RATE_MESSAGE = "Нажмите на маствотч, чтобы поставить ему оценку:"
    __NO_MORE_MUSTWATCHES_TO_RATE_MESSAGE = "Вы уже посмотрели все назначенные вам маствотчи..."
    __RATE_MUSTWATCH_MESSAGE = "Оцените маствотч:"
    __SEND_ITEM_TITLE_MESSAGE = "Отправьте название маствотча:"
    __END_MESSAGE = "Сделано!"

    async def __edit_message_to_choose_user_buttons(self,
                                                    call: CallbackQuery,
                                                    bot_message: str) -> None:
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_choose_user_add_item
        )

    async def __edit_message_to_choose_specific_user_buttons(self,
                                                             call: CallbackQuery,
                                                             bot_message: str,
                                                             user_dict: dict) -> None:
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_choose_specific_user,
            user_dict
        )

    async def __edit_message_to_confirm_request(self,
                                                chat_id: int,
                                                message_id: int,
                                                bot_message: str) -> None:
        await self.edit_message_text_and_buttons(
            chat_id,
            message_id,
            bot_message,
            self.markup_confirm_user_request
        )

    async def __edit_message_to_add_or_delete(self, call: CallbackQuery,
                                              bot_message: str) -> None:
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_add_or_delete_item
        )

    async def __edit_message_to_start_over(self,
                                           call: CallbackQuery,
                                           bot_message: str) -> None:
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_start_over
        )

    async def __edit_message_to_end(self,
                                    call: CallbackQuery,
                                    bot_message: str) -> None:
        await self.edit_message_text_and_delete_buttons(call, bot_message)

    async def __edit_message_to_choose_title(self,
                                             call: CallbackQuery,
                                             bot_message: str,
                                             watches_dict: dict) -> None:
        if watches_dict:
            await self.edit_message_text_and_buttons_from_call(
                call,
                bot_message,
                self.markup_rate_or_delete_title,
                watches_dict
            )
        else:
            await self.__edit_message_to_start_over(call, bot_message)

    async def __edit_message_to_choose_or_add_title(self,
                                                    call: CallbackQuery,
                                                    bot_message: str,
                                                    watches_dict: dict) -> None:
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_choose_or_add_title,
            watches_dict
        )

    async def __edit_message_to_rate_mustwatch_buttons(self,
                                                       call: CallbackQuery,
                                                       bot_message: str) -> None:
        await self.edit_message_text_and_buttons_from_call(
            call,
            bot_message,
            self.markup_rate_mustwatch
        )

    def __get_add_or_delete_word(self,
                                 add_or_delete: bool) -> str:
        if add_or_delete:
            return Button.ADD_BUTTON[0]
        else:
            return Button.DELETE_BUTTON[0] + " из группы"

    async def __get_chosen_user_word(self,
                                     message: Message,
                                     chosen_user: str) -> str:
        if chosen_user == Button.ME_BUTTON_CALLBACK:
            return Button.ME_BUTTON[0].lower()
        elif chosen_user == Button.ALL_BUTTON_CALLBACK:
            return Button.ALL_BUTTON[0].lower()
        else:
            return "пользователю " + await self.get_user_fullname(message.chat.id, int(chosen_user))

    async def start_conversation_with_user(self,
                                           message: Message,
                                           register_state: bool,
                                           chat_id: str,
                                           user_id: str) -> tuple:
        if not register_state:
            await self.bot.reply_to(message,
                                    MustwatchHandler.__USER_IS_NOT_REGISTERED_MESSAGE)
        else:
            msg = await self.bot.reply_to(message,
                                          MustwatchHandler.__ADD_OR_DELETE_MESSAGE,
                                          reply_markup=self.markup_add_or_delete_item())
            return chat_id, user_id, msg.id

    async def edit_add_or_delete_response_to_choose_user_or_title(self,
                                                                  call: CallbackQuery,
                                                                  watches_dict: dict) -> None:
        if call.data == Button.ADD_BUTTON_CALLBACK:
            await self.__edit_message_to_choose_user_buttons(call, MustwatchHandler.__CHOOSE_USER_TO_ADD_MESSAGE)
        else:
            if call.data == Button.DELETE_BUTTON_CALLBACK:
                if watches_dict:
                    bot_message = MustwatchHandler.__CHOOSE_MUSTWATCH_TO_DELETE_MESSAGE
                else:
                    bot_message = MustwatchHandler.__NO_MORE_MUSTWATCHES_TO_DELETE_MESSAGE
            else:
                if watches_dict:
                    bot_message = MustwatchHandler.__CHOOSE_MUSTWATCH_TO_RATE_MESSAGE
                else:
                    bot_message = MustwatchHandler.__NO_MORE_MUSTWATCHES_TO_RATE_MESSAGE
            await self.__edit_message_to_choose_title(call, bot_message, watches_dict)

    async def edit_choose_user_response_to_choose_specific_user(self,
                                                                call: CallbackQuery,
                                                                users_dict: dict) -> None:
        if users_dict:
            bot_message = MustwatchHandler.__CHOOSE_ONE_USER_MESSAGE
        else:
            bot_message = MustwatchHandler.__NO_OTHER_USERS_REGISTERED_MESSAGE
        await self.__edit_message_to_choose_specific_user_buttons(
            call,
            bot_message,
            users_dict
        )

    async def edit_choose_user_response_to_choose_title(self,
                                                        call: CallbackQuery,
                                                        watches_dict: dict) -> None:
        if watches_dict:
            bot_message = MustwatchHandler.__ADD_OR_CHOOSE_MUSTWATCH_MESSAGE
        else:
            bot_message = MustwatchHandler.__NO_MORE_MUSTWATCHES_TO_ADD
        await self.__edit_message_to_choose_or_add_title(call, bot_message,
                                                         watches_dict)

    async def edit_add_or_choose_title_to_send_title(self,
                                                     call: CallbackQuery) -> None:
        await self.edit_message_text_and_delete_buttons(call, MustwatchHandler.__SEND_ITEM_TITLE_MESSAGE)

    async def edit_choose_title_to_confirm_request_or_rate_mustwatch(self, call: CallbackQuery,
                                                                     add_or_delete: bool,
                                                                     chosen_user: str,
                                                                     chat_id: int,
                                                                     message_id: int,
                                                                     bot_message: str) -> None:
        if not add_or_delete and chosen_user == Button.ME_BUTTON_CALLBACK:
            await self.__edit_message_to_rate_mustwatch_buttons(call,
                                                                MustwatchHandler.__RATE_MUSTWATCH_MESSAGE)
        else:
            await self.__edit_message_to_confirm_request(chat_id, message_id, bot_message)

    async def edit_send_title_response_to_confirm_request(self,
                                                          chat_id: int,
                                                          message_id: int,
                                                          bot_message: str) -> None:
        await self.__edit_message_to_confirm_request(chat_id, message_id, bot_message)

    async def edit_send_mustwatch_user_score_response_to_confirm_request(self,
                                                                         chat_id: int,
                                                                         message_id: int,
                                                                         bot_message: int) -> None:
        await self.__edit_message_to_confirm_request(chat_id, message_id, bot_message)

    async def make_bot_message_from_user_request_values(self,
                                                        message: Message,
                                                        add_or_delete: bool,
                                                        title: str,
                                                        chosen_user: str,
                                                        user_score: int) -> str:
        add_or_delete_word = self.__get_add_or_delete_word(add_or_delete)
        title_word = title
        if add_or_delete:
            chosen_user_word = await self.__get_chosen_user_word(message, chosen_user)
        else:
            chosen_user_word = ""
        if user_score:
            user_score_word = str(user_score)
            return "Поставить оценку " + user_score_word + ' "' + title_word + '"?'
        return add_or_delete_word + " " + chosen_user_word + ' "' + title_word + '"?'

    async def edit_confirm_request_response_to_conversation_end(self,
                                                                call: CallbackQuery) -> None:
        if call.data == Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK:
            await self.__edit_message_to_add_or_delete(call, MustwatchHandler.__ADD_OR_DELETE_MESSAGE)
        else:
            await self.__edit_message_to_end(call, MustwatchHandler.__END_MESSAGE)
