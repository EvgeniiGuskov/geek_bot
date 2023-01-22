from typing import Tuple, Dict

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Button:
    DELETE_BUTTON = "Удалить", "delete"
    DELETE_BUTTON_CALLBACK = DELETE_BUTTON[1]
    ADD_BUTTON = "Добавить", "add"
    ADD_BUTTON_CALLBACK = ADD_BUTTON[1]
    SHOW_MUSTWATCHES_BUTTON = "Список моих маствотчей", "my_mustwatches"
    SHOW_MUSTWATCHES_BUTTON_CALLBACK = SHOW_MUSTWATCHES_BUTTON[1]

    ALL_BUTTON = "Всем", "all"
    ALL_BUTTON_CALLBACK = ALL_BUTTON[1]
    ME_BUTTON = "Себе", "me"
    ME_BUTTON_CALLBACK = ME_BUTTON[1]
    CHOOSE_USER_BUTTON = "Другому пользователю", "choose_user"
    CHOOSE_USER_BUTTON_CALLBACK = CHOOSE_USER_BUTTON[1]

    ADD_NEW_MUSTWATCH_BUTTON = "Добавить новый маствотч", "add_new_mustwatch"
    ADD_NEW_MUSTWATCH_BUTTON_CALLBACK = ADD_NEW_MUSTWATCH_BUTTON[1]

    CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK = "users_id_"
    CHOOSE_TITLE_BUTTON_CALLBACK = "watch_id_"
    MUSTWATCH_SCORE_CALLBACK = "mustwatch_score_"

    CHANGE_USER_REQUEST_BUTTON = "Вернуться в начало меню", "change_user_request"
    CHANGE_USER_REQUEST_BUTTON_CALLBACK = CHANGE_USER_REQUEST_BUTTON[1]
    CONFIRM_USER_REQUEST_BUTTON = "Да", "confirm_user_request"
    CONFIRM_USER_REQUEST_BUTTON_CALLBACK = CONFIRM_USER_REQUEST_BUTTON[1]

    START_OVER_BUTTON = "В начало", "start_over"
    START_OVER_BUTTON_CALLBACK = START_OVER_BUTTON[1]
    RECHOOSE_TITLE_BUTTON = "Поменять маствотч", "rechoose_mustwatch"
    RECHOOSE_TITLE_BUTTON_CALLBACK = RECHOOSE_TITLE_BUTTON[1]

    @classmethod
    def markup_add_or_delete_item(cls) -> InlineKeyboardMarkup:
        return cls.__markup_something(
            1,
            Button.ADD_BUTTON,
            Button.SHOW_MUSTWATCHES_BUTTON,
            Button.DELETE_BUTTON
        )

    @classmethod
    def markup_choose_user_add_item(cls,
                                    *args: None) -> InlineKeyboardMarkup:
        return cls.__markup_something(
            2,
            Button.ALL_BUTTON,
            Button.ME_BUTTON,
            Button.CHOOSE_USER_BUTTON
        )

    @classmethod
    def markup_choose_specific_user(cls,
                                    user_dict: Dict[int, str]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        buttons_list = list()
        for key, value in user_dict.items():
            buttons_list.append(InlineKeyboardButton(
                text=value,
                callback_data=Button.CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK + str(key)
            ))
        buttons_list.append(InlineKeyboardButton(
            text=Button.CHANGE_USER_REQUEST_BUTTON[0],
            callback_data=Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK
        ))
        markup.add(*buttons_list)
        return markup

    @classmethod
    def markup_rate_or_delete_title(cls,
                                    watches_dict: Dict[int, str]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        buttons_list = list()
        for key, value in watches_dict.items():
            buttons_list.append(InlineKeyboardButton(
                text=value,
                callback_data=Button.CHOOSE_TITLE_BUTTON_CALLBACK + str(key)
            ))
        buttons_list.append(InlineKeyboardButton(
            text=Button.CHANGE_USER_REQUEST_BUTTON[0],
            callback_data=Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK
        ))
        markup.add(*buttons_list)
        return markup

    @classmethod
    def markup_choose_or_add_title(cls,
                                   watches_dict: Dict[int, str]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        buttons_list = list()
        for key, value in watches_dict.items():
            buttons_list.append(InlineKeyboardButton(
                text=value,
                callback_data=Button.CHOOSE_TITLE_BUTTON_CALLBACK + str(key)
            ))
        buttons_list.append(InlineKeyboardButton(
            text=Button.ADD_NEW_MUSTWATCH_BUTTON[0],
            callback_data=Button.ADD_NEW_MUSTWATCH_BUTTON_CALLBACK
        ))
        buttons_list.append(InlineKeyboardButton(
            text=Button.CHANGE_USER_REQUEST_BUTTON[0],
            callback_data=Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK
        ))
        markup.add(*buttons_list)
        return markup

    @classmethod
    def markup_rate_mustwatch(cls) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        buttons_list = list()
        for i in range(1, 10):
            buttons_list.append(InlineKeyboardButton(
                text=i,
                callback_data=Button.MUSTWATCH_SCORE_CALLBACK + str(i)
            ))
        buttons_list.append(InlineKeyboardButton(
            text=10,
            callback_data=Button.MUSTWATCH_SCORE_CALLBACK + str(10)
        ))
        markup.add(*buttons_list)
        return markup

    @classmethod
    def markup_confirm_user_request(cls) -> InlineKeyboardMarkup:
        return cls.__markup_something(
            2,
            Button.CHANGE_USER_REQUEST_BUTTON,
            Button.CONFIRM_USER_REQUEST_BUTTON
        )

    @classmethod
    def markup_start_over(cls) -> InlineKeyboardMarkup:
        return cls.__markup_something(
            1,
            Button.CHANGE_USER_REQUEST_BUTTON
        )

    @classmethod
    def __make_buttons_list(cls,
                            args: Tuple[str, str]) -> list:
        return [InlineKeyboardButton(args[i][0], callback_data=args[i][1])
                for i in range(len(args))]

    @classmethod
    def __markup_something(cls,
                           row_width: int,
                           *args: Tuple[str, str]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = row_width
        buttons_list = cls.__make_buttons_list(args)
        markup.add(*buttons_list)
        return markup
