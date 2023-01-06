from telebots_potion_store.robots.nanobots.inline_markup_nanobot import InlineMarkupNanobot


class MessageEditorNanobot(InlineMarkupNanobot):

    async def edit_message_text_and_buttons(self, call, text, reply_markup):
        await self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=text,
            reply_markup=reply_markup()
        )

    async def edit_message_text_and_delete_buttons(self, call, text):
        await self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=text
        )
