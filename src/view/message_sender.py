from typing import Dict
from config.telebot.telebot import Telebot
from telebot.types import InlineKeyboardMarkup, CallbackQuery
from telebot.types import CallbackQuery, Message


class MessageSender(Telebot):

    def __init__(self, telebot):
        self.bot = telebot.bot

    async def reply_to_message_with_buttons(self,
                                            message: Message,
                                            bot_message: str,
                                            reply_markup: InlineKeyboardMarkup) -> None:
        return await self.bot.reply_to(message, text=bot_message, reply_markup=reply_markup)

    async def edit_message_text_and_buttons(self,
                                            chat_id: int,
                                            message_id: int,
                                            text: str,
                                            reply_markup: InlineKeyboardMarkup,
                                            *args: Dict[int, str]) -> None:
        await self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup(*args)
        )

    async def edit_message_text_and_buttons_from_call(self,
                                                      call: CallbackQuery,
                                                      text: str,
                                                      reply_markup: InlineKeyboardMarkup,
                                                      *args: Dict[int, str]) -> None:
        await self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=text,
            reply_markup=reply_markup(*args)
        )

    async def edit_message_text_and_delete_buttons(self,
                                                   call: CallbackQuery,
                                                   text: str) -> None:
        await self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=text
        )
