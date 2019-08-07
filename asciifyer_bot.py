import logging
import requests

from io import BytesIO

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image

import config
import modules.ascii_art as asciifyer


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi, send me a quick image (i.e. with compression) to apply some magic!')


def help(update, context):
    update.message.reply_text('Hi, send me a quick image (i.e. with compression) to apply some magic!')


def reply_messages(update, context):
    update.message.reply_text('Processing text messages is not my forte, but to show you my prowess I shall echo what you said.\n\n' +
        '"' + update.message.text + '"')


def convert_photo(update, context):
    update.message.reply_text('Received your image, give me awhile to process.')

    try:
        image = update.message.photo[-1]
        img_file = context.bot.getFile(image.file_id)
        
        try:
            response = requests.get(img_file.file_path)
            image = Image.open(BytesIO(response.content))
        except Exception:
            print ("Unable to find image in", imfile.file_path)
            return

        ascii_image = asciifyer.apply_magic(image)

        # print (ascii_image)

        '''
            * Credits:
                - https://stackoverflow.com/questions/53918409/how-to-send-an-pil-image-via-telegram-bot-without-saving-it-to-a-file
        '''
        bio = BytesIO()
        final_image = asciifyer.string_image(ascii_image)
        final_image.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(bio)
    except:
        update.message.reply_text('Something went wrong and I am unable to convert your image.')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(config.TOKEN, use_context=True)

    '''Deployment'''
    updater.start_webhook(listen="0.0.0.0", port=config.PORT, url_path=config.TOKEN)

    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, reply_messages))
    dp.add_handler(MessageHandler(Filters.photo, convert_photo))

    dp.add_error_handler(error)

    '''Deployment'''
    updater.bot.set_webhook(config.APP_URL + config.TOKEN)

    '''Development'''
    # updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print ("Starting bot...")
    main()
    print ("Bot stopped.")

