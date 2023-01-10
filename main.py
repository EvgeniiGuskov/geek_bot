import database_manager
import telebot_controller

database = database_manager.Alchemist()
telebot = telebot_controller.Telebot()


@telebot.bot.message_handler(commands=["register"])
async def register_user(message):
    user_data = telebot.get_user_data_from_message(message)
    register_result = database.register_user(*user_data)
    await telebot.register_command_response(message, register_result)


@telebot.bot.message_handler(commands=["manage_mustwatch"])
async def add_mustwatch(message):
    user_data = telebot.get_user_data_from_message(message)
    register_state = database.is_user_registered(*user_data)
    user_request_data = await telebot.start_conversation_with_user(message, register_state, *user_data)
    if user_request_data:
        database.update_user_request_message_id(*user_request_data)


def is_callback_protected_from_intruder(call):
    user_data = telebot.get_user_data_and_message_id_from_call(call)
    return database.is_callback_protected_from_intruder(*user_data)


def get_user_add_or_delete(call):
    user_data = telebot.get_user_data_from_call(call)
    return database.get_add_or_delete(*user_data)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data in (telebot.DELETE_BUTTON_CALLBACK,
                                    telebot.ADD_BUTTON_CALLBACK,
                                    telebot.HAS_WATCHED_BUTTON_CALLBACK
                                    )
)
async def chosen_action_on_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = telebot.get_user_choice_from_call(call)
        database.update_user_request_add_or_delete_and_chosen_user(*user_choice)
        add_or_delete = get_user_add_or_delete(call)
        await telebot.edit_add_or_delete_response_to_choose_user(call, add_or_delete)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data in (telebot.ALL_BUTTON_CALLBACK,
                                    telebot.ME_BUTTON_CALLBACK,
                                    telebot.CHOOSE_USER_BUTTON_CALLBACK
                                    )
)
async def choose_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        if call.data in (telebot.ALL_BUTTON_CALLBACK, telebot.ME_BUTTON_CALLBACK):
            user_choice = telebot.get_user_choice_from_call(call)
            database.update_user_request_chosen_user(*user_choice)
            await telebot.edit_choose_user_response_to_choose_title(call)
        else:
            user_data = telebot.get_user_data_from_call(call)
            raw_users_dict = database.get_users_dict(*user_data)
            users_dict = await telebot.convert_telegram_user_id_to_full_name(call, raw_users_dict)
            await telebot.edit_choose_user_response_to_choose_specific_user(call, users_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(telebot.CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = telebot.get_specific_user_choice_from_call(call)
        database.update_user_request_chosen_user(*user_choice)
        await telebot.edit_choose_user_response_to_choose_title(call)


@telebot.bot.callback_query_handler(func=lambda call: call.data == telebot.ADD_NEW_MUSTWATCH_BUTTON_CALLBACK)
async def add_new_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        await telebot.edit_add_or_choose_title_to_send_title(call)
        user_data = telebot.get_user_data_from_call(call)
        database.delete_title_from_user_request(*user_data)


@telebot.bot.message_handler(func=lambda message: len(message.text) < 256)
async def add_title(message):
    user_data = telebot.get_user_data_from_message(message)
    is_user_registered_and_typed_title = database.is_user_registered(
        *user_data) and not database.is_title_filled_at_user_request(
        *user_data)
    if is_user_registered_and_typed_title:
        database.update_user_request_title(*user_data, title=message.text)
        user_request_values = database.get_user_request_values(*user_data)
        bot_message = await telebot.make_bot_message_from_user_request_values(message, *user_request_values)
        message_id = database.get_message_id_from_user_request(*user_data)
        await telebot.edit_send_title_response_to_confirm_request(message.chat.id, message_id, bot_message)


@telebot.bot.callback_query_handler(func=lambda call: call.data in
                                                      (
                                                              telebot.CHANGE_USER_REQUEST_BUTTON_CALLBACK,
                                                              telebot.CONFIRM_USER_REQUEST_BUTTON_CALLBACK)
                                    )
async def change_or_confirm_user_request_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_data = telebot.get_user_data_from_call(call)
        is_user_request_executed = database.execute_user_request(call, *user_data)
        if is_user_request_executed:
            await telebot.edit_confirm_request_response_to_conversation_end(call)


@telebot.bot.callback_query_handler(func=lambda call: call.data in
                                                      (
                                                              telebot.START_OVER_BUTTON_CALLBACK,
                                                              telebot.RECHOOSE_TITLE_BUTTON_CALLBACK
                                                      )
                                    )
async def choose_step_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        await telebot.edit_choose_step_message_response_to_chosen_step(call)


telebot.poll()
