from typing import Dict, Tuple, List, Union
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from telebot.types import CallbackQuery
from src.view.message_text_responses import MessageTextResponse
from src.view.buttons import Button


class MustwatchResponse:

    @staticmethod
    def get_response_to_manage_mustwatch(is_user_registered: bool) -> Tuple[str, Union[InlineKeyboardMarkup, None]]:
        if not is_user_registered:
            return MessageTextResponse.USER_IS_NOT_REGISTERED_MESSAGE, None
        else:
            return MessageTextResponse.ADD_OR_DELETE_MESSAGE, Button.markup_add_or_delete_item()

    @staticmethod
    def get_response_to_add_or_delete(call: CallbackQuery,
                                      watches_dict: Dict[int, str]) -> Tuple[
        str, InlineKeyboardMarkup, Union[Dict[int, str], None]]:
        if call.data == Button.ADD_BUTTON_CALLBACK:
            return MessageTextResponse.CHOOSE_USER_TO_ADD_MESSAGE, Button.markup_choose_user_add_item, None
        elif call.data == Button.DELETE_BUTTON_CALLBACK:
            if watches_dict:
                bot_message = MessageTextResponse.CHOOSE_MUSTWATCH_TO_DELETE_MESSAGE
            else:
                bot_message = MessageTextResponse.NO_MORE_MUSTWATCHES_TO_DELETE_MESSAGE
        else:
            if watches_dict:
                bot_message = MessageTextResponse.CHOOSE_MUSTWATCH_TO_RATE_MESSAGE
            else:
                bot_message = MessageTextResponse.NO_MORE_MUSTWATCHES_TO_RATE_MESSAGE
        button = Button.markup_rate_or_delete_title
        return bot_message, button, watches_dict

    @staticmethod
    def get_response_to_choose_me_or_all(watches_dict: Dict[int, str]) -> Tuple[
        str, InlineKeyboardMarkup, Union[Dict[int, str], None]]:
        if watches_dict:
            bot_message = MessageTextResponse.ADD_OR_CHOOSE_MUSTWATCH_MESSAGE
        else:
            bot_message = MessageTextResponse.NO_MORE_MUSTWATCHES_TO_ADD
        button = Button.markup_choose_or_add_title
        return bot_message, button, watches_dict

    @staticmethod
    def get_response_to_choose_user(users_dict: Dict[int, str]) -> Tuple[
        str, InlineKeyboardMarkup, Union[Dict[int, str], None]]:
        if users_dict:
            bot_message = MessageTextResponse.CHOOSE_ONE_USER_MESSAGE
        else:
            bot_message = MessageTextResponse.NO_OTHER_USERS_REGISTERED_MESSAGE
        button = Button.markup_choose_specific_user
        return bot_message, button, users_dict

    @staticmethod
    def get_response_to_choose_specific_user(watches_dict: Dict[int, str]) -> Tuple[
        str, InlineKeyboardMarkup, Union[Dict[int, str], None]]:
        if watches_dict:
            bot_message = MessageTextResponse.ADD_OR_CHOOSE_MUSTWATCH_MESSAGE
        else:
            bot_message = MessageTextResponse.NO_MORE_MUSTWATCHES_TO_ADD
        button = Button.markup_choose_or_add_title
        return bot_message, button, watches_dict

    @staticmethod
    def get_add_or_delete_word(add_or_delete: bool) -> str:
        if add_or_delete:
            return "Добавить"
        else:
            return "Удалить из группы"

    @staticmethod
    def get_response_to_choose_title(add_or_delete: bool,
                                     title: str,
                                     user_score: int,
                                     chosen_user: str,
                                     chosen_user_word: str) -> str:
        add_or_delete_word = MustwatchResponse.get_add_or_delete_word(add_or_delete)
        title_word = title
        button = Button.markup_confirm_user_request
        if add_or_delete:
            bot_message = add_or_delete_word + " " + chosen_user_word + ' "' + title_word + '"?'
        else:
            bot_message = add_or_delete_word + ' "' + title_word + '"?'
            if chosen_user == Button.ME_BUTTON_CALLBACK:
                if user_score:
                    user_score_word = str(user_score)
                    bot_message = "Поставить оценку " + user_score_word + ' "' + title_word + '"?'
                else:
                    bot_message = MessageTextResponse.RATE_MUSTWATCH_MESSAGE
                    button = Button.markup_rate_mustwatch
        return bot_message, button

    @staticmethod
    def get_response_to_add_new_mustwatch() -> None:
        bot_message = MessageTextResponse.SEND_ITEM_TITLE_MESSAGE
        return bot_message

    @staticmethod
    def get_response_to_confirm_or_change_request(call: CallbackQuery) -> Tuple[str, InlineKeyboardMarkup]:
        if call.data == Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK:
            bot_message = MessageTextResponse.ADD_OR_DELETE_MESSAGE
            button = Button.markup_add_or_delete_item
        else:
            bot_message = MessageTextResponse.END_MESSAGE
            button = Button.markup_start_over
        return bot_message, button
