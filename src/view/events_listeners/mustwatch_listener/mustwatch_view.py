from typing import Dict

from telebot.types import CallbackQuery, Message

from src.view.message_sender import MessageSender
from src.view.events_listeners.mustwatch_listener.mustwatch_response import MustwatchResponse


class MustwatchView:

    def __init__(self, telebot):
        self.msg_sender = MessageSender(telebot)

    async def start_conversation_with_user(self,
                                           message: Message,
                                           is_user_registered: bool) -> int:
        bot_response_content = MustwatchResponse.get_response_to_manage_mustwatch(is_user_registered)
        msg = await self.msg_sender.reply_to_message_with_buttons(message, *bot_response_content)
        return msg.id

    async def answer_to_add_or_delete(self,
                                      call: CallbackQuery,
                                      watches_dict: Dict[int, str]) -> None:
        bot_response_content = MustwatchResponse.get_response_to_add_or_delete(call, watches_dict)
        await self.msg_sender.edit_message_text_and_buttons_from_call(call, *bot_response_content)

    async def answer_to_choose_me_or_all(self,
                                         call: CallbackQuery,
                                         watches_dict: Dict[int, str]) -> None:
        bot_response_content = MustwatchResponse.get_response_to_choose_me_or_all(watches_dict)
        await self.msg_sender.edit_message_text_and_buttons_from_call(call, *bot_response_content)

    async def answer_to_choose_user(self,
                                    call: CallbackQuery,
                                    users_dict: Dict[int, str]) -> None:
        bot_response_content = MustwatchResponse.get_response_to_choose_user(users_dict)
        await self.msg_sender.edit_message_text_and_buttons_from_call(call, *bot_response_content)

    async def answer_to_choose_specific_user(self,
                                             call: CallbackQuery,
                                             watches_dict: Dict[int, str]) -> None:
        bot_response_content = MustwatchResponse.get_response_to_choose_specific_user(watches_dict)
        await self.msg_sender.edit_message_text_and_buttons_from_call(call, *bot_response_content)

    async def answer_to_choose_title(self,
                                     call: CallbackQuery,
                                     add_or_delete: bool,
                                     title: str,
                                     user_score: int,
                                     chosen_user: str,
                                     chosen_user_word: str) -> None:
        bot_response_content = MustwatchResponse.get_response_to_choose_title(add_or_delete,
                                                                              title,
                                                                              user_score,
                                                                              chosen_user,
                                                                              chosen_user_word)
        await self.msg_sender.edit_message_text_and_buttons_from_call(call, *bot_response_content)

    async def answer_to_add_new_mustwatch(self,
                                          call: CallbackQuery) -> None:
        bot_response_content = MustwatchResponse.get_response_to_add_new_mustwatch()
        await self.msg_sender.edit_message_text_and_delete_buttons(call, bot_response_content)

    async def answer_to_typed_title(self,
                                    message: Message,
                                    message_id: int,
                                    add_or_delete: bool,
                                    title: str,
                                    user_score: int,
                                    chosen_user: str,
                                    chosen_user_word: str) -> None:
        bot_response_content = MustwatchResponse.get_response_to_choose_title(add_or_delete,
                                                                              title,
                                                                              user_score,
                                                                              chosen_user,
                                                                              chosen_user_word)
        await self.msg_sender.edit_message_text_and_buttons(message.chat.id, message_id, *bot_response_content)

    async def answer_to_confirm_or_change_request(self,
                                                  call: CallbackQuery) -> None:
        bot_response_content = MustwatchResponse.get_response_to_confirm_or_change_request(call)
        await self.msg_sender.edit_message_text_and_buttons_from_call(call, *bot_response_content)
