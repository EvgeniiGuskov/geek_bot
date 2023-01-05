from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineMarkupNanobot:
    ADD_BUTTON = "Добавить", "add"
    DELETE_BUTTON = "Удалить", "delete"

    ADD_NEW_MUSTWATCH_BUTTON = "Добавить новый маствотч", "new_mustwatch"
    TAKE_MUSWATCH_FROM_DB_BUTTON = "Взять маствотч из группы", "take_mustwatch_from_db"

    TO_ALL_BUTTON = "Всем", "to_all"
    TO_ME_BUTTON = "Мне", "to_me"
    TO_USER_BUTTON = "Другому пользователю", "to_user"

    CINEMA_BUTTON = "Кинематограф", "cinema"
    ANIMATION_BUTTON = "Анимация", "animation"

    FULL_FILM_BUTTON = "Полнометражка", "full_film"
    SHORT_FILM_BUTTON = "Короткометражка", "short_film"
    SERIES_BUTTON = "Сериал", "series"

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

    def markup_add_new_or_take_from_db(self):
        return self.__markup_something(
            2,
            InlineMarkupNanobot.ADD_NEW_MUSTWATCH_BUTTON,
            InlineMarkupNanobot.TAKE_MUSWATCH_FROM_DB_BUTTON
        )

    def markup_to_whom_add_item(self):
        return self.__markup_something(
            2,
            InlineMarkupNanobot.TO_ALL_BUTTON,
            InlineMarkupNanobot.TO_ME_BUTTON,
            InlineMarkupNanobot.TO_USER_BUTTON
        )

    def markup_choose_item_kind(self):
        return self.__markup_something(
            2,
            InlineMarkupNanobot.ANIMATION_BUTTON,
            InlineMarkupNanobot.CINEMA_BUTTON
        )

    def markup_choose_item_timing(self):
        return self.__markup_something(
            2,
            InlineMarkupNanobot.SHORT_FILM_BUTTON,
            InlineMarkupNanobot.FULL_FILM_BUTTON,
            InlineMarkupNanobot.SERIES_BUTTON
        )

