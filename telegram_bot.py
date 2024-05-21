from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import logging
from constants import TELEGRAM_BOT_TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# States for conversation
EMAIL, PASSWORD, SONG_TYPE, CUSTOM_LYRICS, FINAL_PROMPT = range(5)

def start(update: Update, context: CallbackContext) -> int:
    logger.info("Starting conversation, asking for email")
    update.message.reply_text('Please enter your email:')
    return EMAIL

def email(update: Update, context: CallbackContext) -> int:
    logger.info("Received email")
    context.user_data['email'] = update.message.text
    update.message.reply_text('Please enter your password:')
    return PASSWORD

def password(update: Update, context: CallbackContext) -> int:
    logger.info("Received password")
    context.user_data['password'] = update.message.text
    update.message.reply_text('Welcome! Use the /create_song command to start creating a song.')
    return ConversationHandler.END

def create_song(update: Update, context: CallbackContext) -> int:
    logger.info("Starting create_song command")
    keyboard = [
        [InlineKeyboardButton("Custom", callback_data='custom')],
        [InlineKeyboardButton("Auto-generated", callback_data='auto')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose song type:', reply_markup=reply_markup)
    return SONG_TYPE

def song_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.user_data['song_type'] = query.data
    logger.info(f"Song type selected: {query.data}")

    if query.data == 'custom':
        query.edit_message_text(text='Please enter the lyrics for the song:')
        return CUSTOM_LYRICS
    else:
        query.edit_message_text(text='Please enter the prompt for the song:')
        return FINAL_PROMPT

def custom_lyrics(update: Update, context: CallbackContext) -> int:
    logger.info("Received custom lyrics")
    context.user_data['lyrics'] = update.message.text
    update.message.reply_text('Please enter the prompt for the song:')
    return FINAL_PROMPT

def final_prompt(update: Update, context: CallbackContext) -> int:
    logger.info("Received final prompt")
    context.user_data['prompt'] = update.message.text

    song_type = context.user_data['song_type']
    lyrics = context.user_data.get('lyrics', 'N/A')
    prompt = context.user_data['prompt']

    update.message.reply_text(f'Song Type: {song_type}\nLyrics: {lyrics}\nPrompt: {prompt}')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("Conversation cancelled")
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
            SONG_TYPE: [CallbackQueryHandler(song_type)],
            CUSTOM_LYRICS: [MessageHandler(Filters.text & ~Filters.command, custom_lyrics)],
            FINAL_PROMPT: [MessageHandler(Filters.text & ~Filters.command, final_prompt)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('create_song', create_song))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
