from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
from datetime import datetime, timedelta

# Global variables
accounts = []  # List to store Crunchyroll accounts
users = {}  # Dictionary to manage users and their last access time
admins = {6043529845}  # Set to manage admin users
force_channel = '@SikeNezCrunhy'  # Replace with your channel

def check_subscription(update: Update):
    user_id = update.effective_user.id
    chat_member = update.effective_chat.get_member(user_id)
    return chat_member.status in ['member', 'administrator', 'creator']

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {'last_access': None}
    if not check_subscription(update):
        update.message.reply_text("You must join the channel to use this bot.")
        return
    update.message.reply_text("Welcome! You can use the following commands:\n/load <account>\n/get")

def load(update: Update, context: CallbackContext):
    if update.effective_user.id not in admins:
        update.message.reply_text("You are not authorized to use this command.")
        return
    new_account = ' '.join(context.args)
    if new_account:
        accounts.append(new_account)
        update.message.reply_text(f"Account {new_account} loaded successfully!")
    else:
        update.message.reply_text("Please provide an account.")

def get(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in users:
        update.message.reply_text("You must join the channel to use this bot.")
        return
    if not check_subscription(update):
        update.message.reply_text("You must join the channel to use this bot.")
        return

    last_access = users[user_id]['last_access']
    if last_access and datetime.now() < last_access + timedelta(days=2):
        update.message.reply_text("You can request an account again in 2 days.")
        return

    if accounts:
        account = accounts.pop(0)
        users[user_id]['last_access'] = datetime.now()
        update.message.reply_text(f"Here is your Crunchyroll account: {account}")
    else:
        update.message.reply_text("No accounts available.")

def add_admin(update: Update, context: CallbackContext):
    if update.effective_user.id not in admins:
        update.message.reply_text("You are not authorized to use this command.")
        return
    new_admin_id = int(context.args[0])
    admins.add(new_admin_id)
    update.message.reply_text(f"User {new_admin_id} added as admin.")

def remove_admin(update: Update, context: CallbackContext):
    if update.effective_user.id not in admins:
        update.message.reply_text("You are not authorized to use this command.")
        return
    admin_id = int(context.args[0])
    admins.discard(admin_id)
    update.message.reply_text(f"User {admin_id} removed from admin.")

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('load', load))
    dispatcher.add_handler(CommandHandler('get', get))
    dispatcher.add_handler(CommandHandler('addadmin', add_admin))
    dispatcher.add_handler(CommandHandler('removeadmin', remove_admin))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
        
