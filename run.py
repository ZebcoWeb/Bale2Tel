import logging, os, json

from dotenv import load_dotenv

from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram.constants import ParseMode
from telegram import Bot, Update

load_dotenv('.env')

BALE_TOKEN = os.getenv('BALE_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

BALE_BASE_URL = 'https://tapi.bale.ai/bot'
BALE_BASE_FILE_URL = 'https://tapi.bale.ai/file/bot'

f = open('channel_routes.json', 'r')
CHANNEL_ROUTES = json.loads(f.read())
f.close()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class BaleBot(Bot):
    def __init__(self, token):
        super().__init__(
            token,
            base_url=BALE_BASE_URL,
            base_file_url=BALE_BASE_FILE_URL,
        )

bale_app = ApplicationBuilder().bot(BaleBot(BALE_TOKEN)).build()
tel_bot = Bot(TELEGRAM_TOKEN)


async def bale_to_telegram(update: Update, context):
    if update.message:
        channel = update.message.chat.username
        if channel in list(CHANNEL_ROUTES.keys()):
            if update.message.video:
                video = await update.message.video.get_file()
                buffer = await video.download_as_bytearray()

                await tel_bot.send_video(
                    CHANNEL_ROUTES[channel],
                    video=bytes(buffer),
                    caption=update.message.caption,
                    supports_streaming=True,
                )
            elif update.message.photo:
                photo = await update.message.photo[0].get_file()
                buffer = await photo.download_as_bytearray()

                await tel_bot.send_photo(
                    CHANNEL_ROUTES[channel],
                    photo=bytes(buffer),
                    caption=update.message.caption,
                )
            elif update.message.document:
                document = await update.message.document.get_file()
                buffer = await document.download_as_bytearray()

                await tel_bot.send_document(
                    CHANNEL_ROUTES[channel],
                    document=bytes(buffer),
                    caption=update.message.caption,
                )
            else:
                if update.message.text:
                    await tel_bot.send_message(
                        CHANNEL_ROUTES[channel],
                        text=update.message.text,
                        parse_mode=ParseMode.MARKDOWN,
                    )


bale_app.add_handler(
    MessageHandler(
        filters=filters.ALL,
        callback=bale_to_telegram
    )
)

bale_app.run_polling()