class MessageEditorNanobot:
    __TO_WHOM_ADD_MUSTWATCH_MESSAGE = "Кому добавить маствотч?"
    __CHOOSE_ITEM_KIND_MESSAGE = "Что добавить?"
    __ADD_NEW_OR_TAKE_FROM_DATABASE = "Добавить новый маствотч или взять из группы?"
    __CHOOSE_ITEM_TIMING_MESSAGE = "Выбрать хронометраж маствотча"
    __SEND_ITEM_TITLE_MESSAGE = "Напишите название маствотча"


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

    async def edit_message_to_add_new_or_take_from_db_buttons(self, call):
        await self.edit_message_text_and_buttons(
            call,
            MessageEditorNanobot.__ADD_NEW_OR_TAKE_FROM_DATABASE,
            self.markup_add_new_or_take_from_db
        )

    async def edit_message_to_whom_add_item_buttons(self, call):
        await self.edit_message_text_and_buttons(
            call,
            MessageEditorNanobot.__TO_WHOM_ADD_MUSTWATCH_MESSAGE,
            self.markup_to_whom_add_item
        )

    async def edit_message_to_choose_item_kind(self, call):
        await self.edit_message_text_and_buttons(
            call,
            MessageEditorNanobot.__CHOOSE_ITEM_KIND_MESSAGE,
            self.markup_choose_item_kind
        )

    async def edit_message_to_choose_item_timing(self, call):
        await self.edit_message_text_and_buttons(
            call,
            MessageEditorNanobot.__CHOOSE_ITEM_TIMING_MESSAGE,
            self.markup_choose_item_timing
        )

    async def edit_message_to_send_item_title(self, call):
        await self.edit_message_text_and_delete_buttons(call, MessageEditorNanobot.__SEND_ITEM_TITLE_MESSAGE)
