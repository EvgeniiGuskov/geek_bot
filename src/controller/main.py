from telebot.types import CallbackQuery, Message
from src.view.buttons import Button
from config.telebot.telebot import Telebot
from config.database.alchemist import Alchemist
from src.controller.user_data_collector import UserDataCollector
from src.view.commands_handlers.register_handler.register_command_handler import RegisterCommandHandler
from src.view.commands_handlers.mustwatch_rating_handler.mustwatch_rating_command_handler import \
    MustwatchRatingCommandHandler
from src.view.commands_handlers.mustwatch_handler.mustwatch_command_handler import MustwatchCommandHandler
from src.service.register_db import RegisterDb
from src.service.mustwatch_rating_db import MustwatchRatingDb
from src.service.mustwatch_db import MustwatchDb
from src.model.database_checker import DatabaseChecker
from src.model.database_updater import DatabaseUpdater

telebot = Telebot()
user_data_collector = UserDataCollector(telebot)
reg_viewer = RegisterCommandHandler(telebot)
mw_rating_viewer = MustwatchRatingCommandHandler(telebot)
mw_viewer = MustwatchCommandHandler(telebot)

alchemist = Alchemist()
db_check = DatabaseChecker(alchemist)
db_upd = DatabaseUpdater(alchemist)
db_reg = RegisterDb(alchemist, db_check, db_upd)
db_mw_rating = MustwatchRatingDb(alchemist, db_check, db_upd)
db_mw = MustwatchDb(alchemist, db_check, db_upd)


def is_callback_protected_from_intruder(call: CallbackQuery):
    user_data = user_data_collector.get_user_data_and_message_id_from_call(call)
    return db_mw.is_callback_protected_from_intruder(*user_data)


@telebot.bot.message_handler(commands=["register"],
                             chat_types=["private", "group", "supergroup"])
async def register_user(message):
    user_data = user_data_collector.get_user_data_from_message(message)
    db_reg.register_user(*user_data)
    is_user_registered = db_check.is_user_registered(*user_data)
    await reg_viewer.register_command_response(message, is_user_registered)


@telebot.bot.message_handler(commands=["manage_mustwatch"],
                             chat_types=["private", "group", "supergroup"])
async def add_mustwatch(message):
    user_data = user_data_collector.get_user_data_from_message(message)
    is_user_registered = db_check.is_user_registered(*user_data)
    msg_id = await mw_viewer.start_conversation_with_user(message, is_user_registered)
    db_mw.prepare_user_request(*user_data, msg_id)


@telebot.bot.message_handler(commands=["mustwatch_rating"],
                             chat_types=["private", "group", "supergroup"])
async def show_mustwatch_rating(message):
    chat_id = user_data_collector.get_chat_id_from_message(message)
    rated_watches_dict = db_mw_rating.get_rated_watches_dict(chat_id)
    await mw_rating_viewer.send_mustwatches_rating(message, rated_watches_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data in (Button.DELETE_BUTTON_CALLBACK,
                                    Button.ADD_BUTTON_CALLBACK,
                                    Button.SHOW_MUSTWATCHES_BUTTON_CALLBACK
                                    )
)
async def chosen_action_on_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = user_data_collector.get_user_choice_from_call(call)
        user_data = user_data_collector.get_user_data_from_call(call)
        db_mw.update_user_request_add_or_delete_and_chosen_user(*user_choice)
        watches_dict = db_mw.get_watches_dict(*user_data)
        await mw_viewer.answer_to_add_or_delete(call, watches_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data in (Button.ALL_BUTTON_CALLBACK,
                                    Button.ME_BUTTON_CALLBACK,
                                    Button.CHOOSE_USER_BUTTON_CALLBACK
                                    )
)
async def choose_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        if call.data in (Button.ALL_BUTTON_CALLBACK, Button.ME_BUTTON_CALLBACK):
            user_choice = user_data_collector.get_user_choice_from_call(call)
            user_data = user_data_collector.get_user_data_from_call(call)
            db_mw.update_user_request_chosen_user_id_transaction(*user_choice)
            watches_dict = db_mw.get_watches_dict(*user_data)
            await mw_viewer.answer_to_choose_me_or_all(call, watches_dict)
        else:
            user_data = user_data_collector.get_user_data_from_call(call)
            raw_users_dict = db_mw.get_users_dict(*user_data)
            users_dict = await user_data_collector.convert_telegram_user_id_to_full_name(call, raw_users_dict)
            await mw_viewer.answer_to_choose_user(call, users_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(Button.CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = user_data_collector.get_specific_user_choice_from_call(call)
        user_data = user_data_collector.get_user_data_from_call(call)
        db_mw.update_user_request_chosen_user_id_transaction(*user_choice)
        watches_dict = db_mw.get_watches_dict(*user_data)
        await mw_viewer.answer_to_choose_specific_user(call, watches_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(Button.CHOOSE_TITLE_BUTTON_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = user_data_collector.get_title_choice_from_call(call)
        user_data = user_data_collector.get_user_data_from_call(call)
        db_mw.update_user_request_chosen_title(*user_choice)
        user_request_vals = db_mw.get_user_request_values(*user_data)
        chosen_user = db_mw.get_chosen_user_from_user_request(*user_data)
        chosen_user_word = await user_data_collector.get_chosen_user_word(call.message, chosen_user)
        await mw_viewer.answer_to_choose_title(call, *user_request_vals, chosen_user, chosen_user_word)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(Button.MUSTWATCH_SCORE_CALLBACK)
)
async def mustwatch_score_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = user_data_collector.get_user_score_choice_from_call(call)
        user_data = user_data_collector.get_user_data_from_call(call)
        db_mw.update_user_request_user_score_transaction(*user_choice)
        user_request_vals = db_mw.get_user_request_values(*user_data)
        chosen_user = db_mw.get_chosen_user_from_user_request(*user_data)
        chosen_user_word = await user_data_collector.get_chosen_user_word(call.message, chosen_user)
        await mw_viewer.answer_to_choose_title(call, *user_request_vals, chosen_user, chosen_user_word)


@telebot.bot.callback_query_handler(func=lambda call: call.data == Button.ADD_NEW_MUSTWATCH_BUTTON_CALLBACK)
async def add_new_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_data = user_data_collector.get_user_data_from_call(call)
        db_mw.delete_title_from_user_request(*user_data)
        await mw_viewer.answer_to_add_new_mustwatch(call)


@telebot.bot.message_handler(func=lambda message: len(message.text) < 256,
                             chat_types=["private", "group", "supergroup"])
async def add_title(message):
    user_data = user_data_collector.get_user_data_from_message(message)
    is_user_registered_and_typed_title = db_mw.is_user_registered_and_title_is_not_filled(*user_data)
    if is_user_registered_and_typed_title:
        db_mw.update_user_request_title_transaction(*user_data, message.text)
        user_request_vals = db_mw.get_user_request_values(*user_data)
        chosen_user = db_mw.get_chosen_user_from_user_request(*user_data)
        chosen_user_word = await user_data_collector.get_chosen_user_word(message, chosen_user)
        message_id = db_mw.get_message_id_from_user_request(*user_data)
        await mw_viewer.answer_to_typed_title(message, message_id, *user_request_vals, chosen_user, chosen_user_word)


@telebot.bot.callback_query_handler(func=lambda call: call.data in
                                                      (
                                                              Button.CHANGE_USER_REQUEST_BUTTON_CALLBACK,
                                                              Button.CONFIRM_USER_REQUEST_BUTTON_CALLBACK)
                                    )
async def change_or_confirm_user_request_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_data = user_data_collector.get_user_data_from_call(call)
        db_mw.execute_user_request(call, *user_data)
        await mw_viewer.answer_to_confirm_or_change_request(call)


telebot.poll()
