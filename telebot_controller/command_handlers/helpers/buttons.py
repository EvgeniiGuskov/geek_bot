from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Button:
    DELETE_BUTTON = "Удалить маствотч из группы", "delete"
    DELETE_BUTTON_CALLBACK = DELETE_BUTTON[1]
    ADD_BUTTON = "Добавить маствотч", "add"
    ADD_BUTTON_CALLBACK = ADD_BUTTON[1]
    HAS_WATCHED_BUTTON = "Поставить оценку маствотчу", "watched"
    HAS_WATCHED_BUTTON_CALLBACK = HAS_WATCHED_BUTTON[1]

    ALL_BUTTON = "Всем", "all"
    ALL_BUTTON_CALLBACK = ALL_BUTTON[1]
    ME_BUTTON = "Себе", "me"
    ME_BUTTON_CALLBACK = ME_BUTTON[1]
    CHOOSE_USER_BUTTON = "Другому пользователю", "choose_user"
    CHOOSE_USER_BUTTON_CALLBACK = CHOOSE_USER_BUTTON[1]

    ADD_NEW_MUSTWATCH_BUTTON = "Добавить новый маствотч", "add_new_mustwatch"
    ADD_NEW_MUSTWATCH_BUTTON_CALLBACK = ADD_NEW_MUSTWATCH_BUTTON[1]

    CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK = "users_id_"

    CHANGE_USER_REQUEST_BUTTON = "Нет", "change_user_request"
    CHANGE_USER_REQUEST_BUTTON_CALLBACK = CHANGE_USER_REQUEST_BUTTON[1]
    CONFIRM_USER_REQUEST_BUTTON = "Да", "confirm_user_request"
    CONFIRM_USER_REQUEST_BUTTON_CALLBACK = CONFIRM_USER_REQUEST_BUTTON[1]

    START_OVER_BUTTON = "В начало", "start_over"
    START_OVER_BUTTON_CALLBACK = START_OVER_BUTTON[1]
    RECHOOSE_TITLE_BUTTON = "Поменять маствотч", "rechoose_mustwatch"
    RECHOOSE_TITLE_BUTTON_CALLBACK = RECHOOSE_TITLE_BUTTON[1]

    def __make_buttons_list(self, args):
        return [InlineKeyboardButton(args[i][0], callback_data=args[i][1])
                for i in range(len(args))]

    def __markup_something(self, row_width, *args):
        markup = InlineKeyboardMarkup()
        markup.row_width = row_width
        buttons_list = self.__make_buttons_list(args)
        markup.add(*buttons_list)
        return markup

    def markup_add_or_delete_item(self):
        return self.__markup_something(
            1,
            Button.ADD_BUTTON,
            Button.HAS_WATCHED_BUTTON,
            Button.DELETE_BUTTON
        )

    def markup_choose_user_add_item(self):
        return self.__markup_something(
            2,
            Button.ALL_BUTTON,
            Button.ME_BUTTON,
            Button.CHOOSE_USER_BUTTON
        )

    def markup_choose_specific_user(self, user_dict):
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        buttons_list = list()
        for key, value in user_dict.items():
            buttons_list.append(InlineKeyboardButton(
                text=value,
                callback_data=Button.CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK + str(key)
            ))
        markup.add(*buttons_list)
        return markup

    def markup_choose_title(self):
        return self.__markup_something(
            1,
            Button.ADD_NEW_MUSTWATCH_BUTTON
        )

    def markup_confirm_user_request(self):
        return self.__markup_something(
            2,
            Button.CHANGE_USER_REQUEST_BUTTON,
            Button.CONFIRM_USER_REQUEST_BUTTON
        )

    def markup_choose_step(self):
        return self.__markup_something(
            1,
            Button.START_OVER_BUTTON,
            Button.RECHOOSE_TITLE_BUTTON
        )
