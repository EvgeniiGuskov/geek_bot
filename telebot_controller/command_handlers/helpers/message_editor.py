from telebot_controller.command_handlers.helpers.buttons import Button


class MessageEditor(Button):

    async def edit_message_text_and_buttons(self, chat_id, message_id, text, reply_markup, *args):
        await self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup(*args)
        )

    async def edit_message_text_and_buttons_from_call(self, call, text, reply_markup, *args):
        await self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=text,
            reply_markup=reply_markup(*args)
        )

    async def edit_message_text_and_delete_buttons(self, call, text):
        await self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=text
        )
