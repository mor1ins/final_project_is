import logging
import os
import random
import re
import shutil
import subprocess
import time

import aiml
from google_images_download import google_images_download
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import tts_tools as tts
from config import TOKEN

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
    voice = f'{output_file}.ogg'
    context.bot.send_voice(chat_id=chat_id, voice=open(voice, 'rb'))
    os.remove(voice)


def start(update, context):
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    print(f'Received message "{update.message.text}" from {update.message.chat.id}')
    response = aiml_kernel.respond(update.message.text)
    command_pattern = r"\*\*\*\w+\s*\w*\*\*\*"
    search = re.search(command_pattern, response)
    if search is not None:
        response = re.sub(command_pattern, '', response)
        keywords = search.group()[3:-3]
        subprocess.run(["googleimagesdownload", "--keywords", keywords, "--limit",  "10", "-o", "image/"])

    update.message.reply_text(response)
    say(response, update.message.chat.id, context)
    print(f'Sent message "{response}" to {update.message.chat.id}')
    image_path = 'image/'
    for directory in os.listdir(image_path):
        dir_path = os.path.join(image_path, directory)
        photos = [os.path.join(dir_path, photo) for photo in os.listdir(dir_path)]
        context.bot.send_photo(chat_id=update.message.chat.id, photo=open(random.choice(photos), 'rb'))
        shutil.rmtree(dir_path)


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
