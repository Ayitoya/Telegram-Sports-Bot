import requests
from bs4 import BeautifulSoup
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Initialize Telegram bot and token
bot = telegram.Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)

# Define function to get matches and scores from website
def get_scores(league):
    url = f'https://www.example.com/{league}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scores = soup.find_all(class_='score')
    matches = soup.find_all(class_='match')
    return scores, matches

# Define function to send scores and matches to Telegram channel
def send_scores(bot, update, league):
    chat_id = update.message.chat_id
    scores, matches = get_scores(league)
    message = f'Latest {league} matches:\n'
    for i in range(len(scores)):
        score = scores[i].get_text()
        match = matches[i].get_text()
        message += f'{match}: {score}\n'
    bot.send_message(chat_id=chat_id, text=message)

# Define function to create menu of leagues for users to choose from
def leagues_menu(bot, update):
    chat_id = update.message.chat_id
    keyboard = [
        [InlineKeyboardButton("Premier League", callback_data='pl'),
         InlineKeyboardButton("La Liga", callback_data='ll')],
        [InlineKeyboardButton("Serie A", callback_data='sa'),
         InlineKeyboardButton("Bundesliga", callback_data='bl')],
        [InlineKeyboardButton("Ligue 1", callback_data='l1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text='Choose a league to get scores from:', reply_markup=reply_markup)

# Define function to handle user input from menu
def button_handler(bot, update):
    query = update.callback_query
    league = query.data
    send_scores(bot, update, league)
    query.edit_message_text(text=f'You chose {league}')

# Define Telegram bot commands and handlers
def start(bot, update):
    update.message.reply_text('Hi, I am a sports news bot! Type /scores to get the latest scores or /leagues to choose a league.')
    
def scores(bot, update):
    chat_id = update.message.chat_id
    message = 'Which league do you want scores from?'
    bot.send_message(chat_id=chat_id, text=message)
    
def leagues(bot, update):
    leagues_menu(bot, update)

# Add handlers to Telegram bot
start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(start_handler)

scores_handler = CommandHandler('scores', scores)
updater.dispatcher.add_handler(scores_handler)

leagues_handler = CommandHandler('leagues', leagues)
updater.dispatcher.add_handler(leagues_handler)

button_handler = CallbackQueryHandler(button_handler)
updater.dispatcher.add_handler(button_handler)

# Start the bot
updater.start_polling()
updater.idle()
