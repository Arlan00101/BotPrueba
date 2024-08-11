import logging
from telegram.constants import ParseMode
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)

screaming = False

FIRST_MENU = "<b>Quiere hacer una petición:</b>\n\nAl presionar (Si) realizará una petición, en cambio si presiona (No) no pasará nada."
SECOND_MENU = "<b>Ya ha realizado la petición</b>\n\nPresione no para volver."

NEXT_BUTTON = "Si"
BACK_BUTTON = "No"
TUTORIAL_BUTTON = "Tutorial"

FIRST_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)
]])

SECOND_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON),
    InlineKeyboardButton(TUTORIAL_BUTTON, callback_data=TUTORIAL_BUTTON),
]])

def echo(update: Update, context: CallbackContext) -> None:
    
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if screaming and update.message.text:
        print(update.message.chat_id)
        context.bot.send_message(
            '1448571421',
            update.message.text.upper(),
            entities = update.message.entities
        )
    else:
        update.message.copy('1448571421')

def scream(update: Update, context: CallbackContext) -> None:
    global screaming
    screaming = True

def whisper(update: Update, context: CallbackContext) -> None:
    global screaming
    screaming = False

def menu(update: Update, context: CallbackContext) -> None:
    
    context.bot.send_message(
        update.message.from_user.id,
        FIRST_MENU,
        parse_mode = ParseMode.HTML,
        reply_markup = FIRST_MENU_MARKUP
    )

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
        KeyboardButton('/scream'),
        KeyboardButton('/whisper')
        ], 
        [KeyboardButton('/menu')]
        ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Selecciona una acción:', reply_markup=reply_markup)

def button_tap(update: Update, context: CallbackContext) -> None:

    data = update.callback_query.data
    text = ''
    markup = None
    if data == NEXT_BUTTON:
        context.bot.send_message(
            '1448571421',
            f'El usuario {update.callback_query.from_user.full_name}',
        )
        context.bot.send_photo(
            '1448571421',
            update.callback_query.from_user.get_profile_photos().photos[0][0].file_id,
        )
        context.bot.send_message(
            '1448571421',
            f'Ha enviado una petición',
        )
        text = SECOND_MENU
        markup = SECOND_MENU_MARKUP
    elif data == BACK_BUTTON:
        text = FIRST_MENU
        markup = FIRST_MENU_MARKUP
    
    update.callback_query.answer()

    update.callback_query.message.edit_text(
        text,
        ParseMode.HTML,
        reply_markup=markup
    )


def main() -> None:
    updater = Updater("7475055123:AAFvEZy_GwlWnlKsEeXbRpNqe5oi5r5Yc7I")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("scream", scream))
    dispatcher.add_handler(CommandHandler("whisper", whisper))
    dispatcher.add_handler(CommandHandler("menu", menu))

    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
