from telebot.types import InlineKeyboardMarkup, CallbackQuery


class MessageEditor:

    async def edit_message_text_and_buttons(self,
                                            chat_id: int,
                                            message_id: int,
                                            text: str,
                                            reply_markup: InlineKeyboardMarkup,
                                            *args: dict) -> None:
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
                                                      *args: dict) -> None:
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
