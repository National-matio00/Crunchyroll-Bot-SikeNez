import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from time import time
from functools import wraps

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set your bot token and other variables
BOT_TOKEN = '7879690371:AAHGgAVoLe92D-r3vTs4I7oUGAcwDaG6p70'
FORCE_SUB_CHANNEL = '@SikeNezCrunhy'  # Use the username, not the full URL
COOLDOWN = 7200  # 2 hours in seconds

accounts = []
user_cooldowns = {}
admins = [6043529845]  # Add your Telegram user ID as the initial admin

# Check for forced subscription
def is_user_subscribed(user_id):
    # Placeholder for checking user subscription
    return True  # Implement actual check if needed

# Cooldown decorator
def cooldown_required(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        if user_id in user_cooldowns:
            if time() - user_cooldowns[user_id] < COOLDOWN:
                update.message.reply_text("You need to wait before claiming another account.")
                return
        return func(update, context)
    return wrapper

@cooldown_required
def get_crunchyroll(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if not is_user_subscribed(user_id):
        update.message.reply_text(f"You must subscribe to {FORCE_SUB_CHANNEL} to use this command.")
        return

    if accounts:
        account = accounts.pop(0)
        user_cooldowns[user_id] = time()  # Update cooldown for user
        update.message.reply_text(f"Here is your Crunchyroll account: {account}")
    else:
        update.message.reply_text("No accounts available at the moment.")

def load_account(update: Update, context: CallbackContext):
    if update.message.from_user.id not in admins:
        update.message.reply_text("You are not authorized to use this command.")
        return

    account = ' '.join(context.args)
    accounts.append(account)
    update.message.reply_text(f"Account loaded: {account}")

def add_admin(update: Update, context: CallbackContext):
    if update.message.from_user.id != 6043529845:  # Replace with your Telegram user ID
        update.message.reply_text("You are not authorized to add admins.")
        return

    new_admin_id = int(context.args[0])
    if new_admin_id not in admins:
        admins.append(new_admin_id)
        update.message.reply_text(f"Admin added: {new_admin_id}")
    else:
        update.message.reply_text("This user is already an admin.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("GetCrunchyroll", get_crunchyroll))
    dp.add_handler(CommandHandler("load", load_account))
    dp.add_handler(CommandHandler("addadmin", add_admin))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
