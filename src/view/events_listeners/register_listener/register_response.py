from src.view.message_text_responses import MessageTextResponse


class RegisterResponse:

    @staticmethod
    def get_response_to_register(is_user_registered: bool) -> str:
        if is_user_registered:
            return MessageTextResponse.USER_IS_REGISTERED_MESSAGE
        else:
            return MessageTextResponse.OOPS_MESSAGE
