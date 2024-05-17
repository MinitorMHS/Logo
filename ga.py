from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bs4 import BeautifulSoup
import requests

# Replace 'your_token' with your actual Telegram bot token
TOKEN = 'your_token'

# The chat ID where you want to send the notification
CHAT_ID = 'your_chat_id'

# URL of the page to monitor
URL = 'https://www.parsdata.com/free-domain'

# The last known value of the promo code
last_known_promo_code = ''

def check_promo_code(update, context):
    global last_known_promo_code
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    promo_code_element = soup.select_one('.fdCode > span[style="color: #00b050;"]')
    new_promo_code = promo_code_element.get_text(strip=True) if promo_code_element else 'Not Found'
    
    if new_promo_code != last_known_promo_code:
        last_known_promo_code = new_promo_code
        context.bot.send_message(chat_id=CHAT_ID, text=f'Promo code changed to: {new_promo_code}')

def main():
    application = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler('start', lambda update, context: update.message.reply_text('Hello! I am your promo code monitoring bot.'))
    online_handler = CommandHandler('online', lambda update, context: update.message.reply_text('I am online and ready!'))
    current_code_handler = CommandHandler('currentcode', lambda update, context: update.message.reply_text(f'The current promo code is: {last_known_promo_code}'))
    check_promo_code_handler = MessageHandler(filters.COMMAND, check_promo_code)

    application.add_handler(start_handler)
    application.add_handler(online_handler)
    application.add_handler(current_code_handler)
    application.add_handler(check_promo_code_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
