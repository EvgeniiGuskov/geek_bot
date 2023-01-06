from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineMarkupNanobot:
    DELETE_BUTTON = "Удалить", "delete"
    ADD_BUTTON = "Добавить", "add"

    ALL_BUTTON = "Всем", "all"
    ME_BUTTON = "Мне", "me"
    CHOOSE_USER_BUTTON = "Другому пользователю", "choose_user"

    ADD_NEW_MUSTWATCH_BUTTON = "Добавить новый маствотч", "new_mustwatch"

    def __make_buttons_list(self, args):
        return [InlineKeyboardButton(args[i][0], callback_data=args[i][1])
                for i in range(len(args))]

    def __markup_something(self, row_width, *args):
        markup = InlineKeyboardMarkup()
        markup.row_width = row_width

        buttons_list = self.__make_buttons_list(args)

        markup.add(
            *buttons_list
        )
        return markup

    def markup_add_or_delete_item(self):
        return self.__markup_something(
            2,
            InlineMarkupNanobot.DELETE_BUTTON,
            InlineMarkupNanobot.ADD_BUTTON
        )
    def markup_choose_user_add_item(self):
        return self.__markup_something(
            2,
            InlineMarkupNanobot.ALL_BUTTON,
            InlineMarkupNanobot.ME_BUTTON,
            InlineMarkupNanobot.CHOOSE_USER_BUTTON
        )
