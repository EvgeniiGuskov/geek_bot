from telebot.types import CallbackQuery

from src.view.buttons import Button
from src.controller.app import App

app = App()


def is_callback_protected_from_intruder(call: CallbackQuery) -> bool:
    user_data = app.telebot_adapter.get_user_data_and_message_id_from_call(call)
    return app.db_mw.is_callback_protected_from_intruder(*user_data)


@app.telebot.bot.message_handler(commands=["register"],
                                 chat_types=["group", "supergroup"])
async def register_user(message):
    user_data = app.telebot_adapter.get_user_data_from_message(message)
    app.db_reg.register_user(*user_data)
    is_user_registered = app.users_read.is_user_registered(*user_data)
    await app.reg_viewer.register_command_response(message, is_user_registered)


@app.telebot.bot.message_handler(commands=["manage_mustwatch"],
                                 chat_types=["group", "supergroup"])
async def add_mustwatch(message):
    user_data = app.telebot_adapter.get_user_data_from_message(message)
    is_user_registered = app.users_read.is_user_registered(*user_data)
    msg_id = await app.mw_viewer.start_conversation_with_user(message, is_user_registered)
    app.db_mw.prepare_user_request(*user_data, msg_id)


@app.telebot.bot.message_handler(commands=["mustwatch_rating"],
                                 chat_types=["group", "supergroup"])
async def show_mustwatch_rating(message):
    chat_id = app.telebot_adapter.get_chat_id_from_message(message)
    rated_watches_dict = app.db_mw_rating.get_rated_watches_dict(chat_id)
    await app.mw_rating_viewer.send_mustwatches_rating(message, rated_watches_dict)


@app.telebot.bot.callback_query_handler(
    func=lambda call: call.data in (Button.DELETE_BUTTON_CALLBACK,
                                    Button.ADD_BUTTON_CALLBACK,
                                    Button.SHOW_MUSTWATCHES_BUTTON_CALLBACK
                                    )
)
async def chosen_action_on_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = app.telebot_adapter.get_user_choice_from_call(call)
        user_data = app.telebot_adapter.get_user_data_from_call(call)
        app.db_mw.update_user_request_add_or_delete_and_chosen_user(*user_choice)
        watches_dict = app.db_mw.get_watches_dict(*user_data)
        await app.mw_viewer.answer_to_add_or_delete(call, watches_dict)


@app.telebot.bot.callback_query_handler(
    func=lambda call: call.data in (Button.ALL_BUTTON_CALLBACK,
                                    Button.ME_BUTTON_CALLBACK,
                                    Button.CHOOSE_USER_BUTTON_CALLBACK
                                    )
)
async def choose_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        if call.data in (Button.ALL_BUTTON_CALLBACK, Button.ME_BUTTON_CALLBACK):
            user_choice = app.telebot_adapter.get_user_choice_from_call(call)
            user_data = app.telebot_adapter.get_user_data_from_call(call)
            app.db_mw.update_user_request_chosen_user_id_transaction(*user_choice)
            watches_dict = app.db_mw.get_watches_dict(*user_data)
            await app.mw_viewer.answer_to_choose_me_or_all(call, watches_dict)
        else:
            user_data = app.telebot_adapter.get_user_data_from_call(call)
            raw_users_dict = app.db_mw.get_users_dict(*user_data)
            users_dict = await app.telebot_adapter.convert_telegram_user_id_to_full_name(call, raw_users_dict)
            await app.mw_viewer.answer_to_choose_user(call, users_dict)


@app.telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(Button.CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = app.telebot_adapter.get_specific_user_choice_from_call(call)
        user_data = app.telebot_adapter.get_user_data_from_call(call)
        app.db_mw.update_user_request_chosen_user_id_transaction(*user_choice)
        watches_dict = app.db_mw.get_watches_dict(*user_data)
        await app.mw_viewer.answer_to_choose_specific_user(call, watches_dict)


@app.telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(Button.CHOOSE_TITLE_BUTTON_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = app.telebot_adapter.get_title_choice_from_call(call)
        user_data = app.telebot_adapter.get_user_data_from_call(call)
        app.db_mw.update_user_request_chosen_title(*user_choice)
        user_request_vals = app.db_mw.get_user_request_values(*user_data)
        chosen_user = app.db_mw.get_chosen_user_from_user_request(*user_data)
        chosen_user_word = await app.telebot_adapter.get_chosen_user_word(call.message, chosen_user)
        await app.mw_viewer.answer_to_choose_title(call, *user_request_vals, chosen_user, chosen_user_word)


@app.telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(Button.MUSTWATCH_SCORE_CALLBACK)
)
async def mustwatch_score_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = app.telebot_adapter.get_user_score_choice_from_call(call)
        user_data = app.telebot_adapter.get_user_data_from_call(call)
        app.db_mw.update_user_request_user_score_transaction(*user_choice)
        user_request_vals = app.db_mw.get_user_request_values(*user_data)
        chosen_user = app.db_mw.get_chosen_user_from_user_request(*user_data)
        chosen_user_word = await app.telebot_adapter.get_chosen_user_word(call.message, chosen_user)
        await app.mw_viewer.answer_to_choose_title(call, *user_request_vals, chosen_user, chosen_user_word)


@app.telebot.bot.callback_query_handler(func=lambda call: call.data == Button.ADD_NEW_MUSTWATCH_BUTTON_CALLBACK)
async def add_new_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_data = app.telebot_adapter.get_user_data_from_call(call)
        app.db_mw.delete_title_from_user_request(*user_data)
        await app.mw_viewer.answer_to_add_new_mustwatch(call)


@app.telebot.bot.message_handler(func=lambda message: len(message.text) < 256,
                                 chat_types=["group", "supergroup"])
async def add_title(message):
    user_data = app.telebot_adapter.get_user_data_from_message(message)
    is_user_registered_and_typed_title = app.db_mw.is_user_registered_and_title_is_not_filled(*user_data)
    if is_user_registered_and_typed_title:
        app.db_mw.update_user_request_title_transaction(*user_data, message.text)
        user_request_vals = app.db_mw.get_user_request_values(*user_data)
        chosen_user = app.db_mw.get_chosen_user_from_user_request(*user_data)
        chosen_user_word = await app.telebot_adapter.get_chosen_user_word(message, chosen_user)
        message_id = app.db_mw.get_message_id_from_user_request(*user_data)
        await app.mw_viewer.answer_to_typed_title(message, message_id, *user_request_vals, chosen_user,
                                                  chosen_user_word)


@app.telebot.bot.callback_query_handler(func=lambda call: call.data in
                                                          (
                                                                  Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK,
                                                                  Button.CONFIRM_USER_REQUEST_BUTTON_CALLBACK)
                                        )
async def change_or_confirm_user_request_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_data = app.telebot_adapter.get_user_data_from_call(call)
        app.db_mw.execute_user_request(call, *user_data)
        await app.mw_viewer.answer_to_confirm_or_change_request(call)
