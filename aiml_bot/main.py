import logging
import time
import aiml

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import TOKEN
import tts_tools as tts

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

aiml_kernel = aiml.Kernel()
aiml_kernel.learn("std-startup.xml")
aiml_kernel.respond("load aiml b")


def say(text, chat_id, context):
    output_file = f'audio/{chat_id}_{int(time.time())}'
    tts.text_to_voice(text, 'ru', output_file)
    context.bot.send_voice(chat_id=chat_id, voice=open(f'{output_file}.ogg', 'rb'))


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    print(f'Received message "{update.message.text}" from {update.message.chat.id}')
    say(aiml_kernel.respond(update.message.text), update.message.chat.id, context)
    print(f'Sent message to {update.message.chat.id}')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    print('Starting...')
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
