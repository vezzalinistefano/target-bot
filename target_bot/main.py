import os
import logging
from custom_filters import TargetUserFilter, AllowedUserFilter
from phrases import add_new_phrase, get_random_phrase
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    filters, MessageHandler, ApplicationBuilder,
    ContextTypes, CommandHandler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def add_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message.from_user.id == int(TARGET_USER_ID)):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Bel tentativo, ma purtroppo non puoi!",
                                       reply_to_message_id=update.message.id
                                       )
        return

    phrase = " ".join(context.args)
    if not phrase or phrase.isspace():
        return

    logging.log(logging.INFO, f"Adding phrase:  {phrase}")

    add_result = await add_new_phrase(phrase)
    if add_result:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Nuova frase aggiunta correttamente"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="La frase è già presente"
        )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.log(
        logging.INFO, f"Username: {update.message.from_user.username}, Id: {update.message.from_user.id}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.log(logging.INFO, "Sending a message to the target user")
    phrase = await get_random_phrase()

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=phrase,
                                   reply_to_message_id=update.message.id
                                   )


if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    TARGET_USER_ID = os.getenv("TARGET_USER_ID")
    logging.log(logging.INFO, TARGET_USER_ID)

    application = ApplicationBuilder().token(TOKEN).build()

    add_phrase_handler = CommandHandler(
        'add', add_phrase,
    )
    echo_handler = MessageHandler(TargetUserFilter(TARGET_USER_ID), echo)

    info_handler = MessageHandler(filters.TEXT, info)
    application.add_handler(add_phrase_handler)
    application.add_handler(echo_handler)
    application.add_handler(info_handler)

    application.run_polling()
