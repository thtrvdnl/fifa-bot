from environs import Env
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
)

import utils
import services

env = Env()
env.read_env()


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ну что погнали !\n"
        "/pop - id token minimum_price maximum_price time\n"
        "Example:\n"
        "/pop 1215 5as1dasd52215sa 500 10000 1",
    )


def redeem_player(update: Update, context: CallbackContext) -> None:
    try:
        valid_context = services.validate_context_for_player(context.args)
        player = utils.Player(*valid_context)
        result = services.start_asking_player(player)
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)

    except utils.AuthError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Неверные данные пользователя",
        )

    except utils.ListLengthError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Неправильно введены данные",
        )

    except NetworkError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ошибка соединения телеграмма",
        )


def main() -> None:
    """Start the bot."""
    updater = Updater(token=env.str("TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pop", redeem_player))

    updater.start_polling()


if __name__ == "__main__":
    main()
