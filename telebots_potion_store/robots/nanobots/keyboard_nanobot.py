from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardNanobot:
    def markup_whom_add(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(
            InlineKeyboardButton("Всем", callback_data="all"),
            InlineKeyboardButton("Мне", callback_data="me"),
            InlineKeyboardButton("Участнику", callback_data="user")
        )
        return markup
