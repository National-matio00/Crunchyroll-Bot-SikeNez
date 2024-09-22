import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from time import time
from functools import wraps

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set your bot token here
BOT_TOKEN = 'YOUR_BOT_TOKEN'
FORCE_SUB_CHANNEL = '@your_channel'  # Change to your channel username
COOLDOWN = 7200  # 2 hours in seconds

accounts = []
user_cooldowns = {}

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
    if update.message.from_user.id not in [OWNER_ID, ADMIN_ID]:  # Replace with actual owner/admin IDs
        update.message.reply_text("You are not authorized to use this command.")
        return

    account = ' '.join(context.args)
    accounts.append(account)
    update.message.reply_text(f"Account loaded: {account}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("GetCrunchyroll", get_crunchyroll))
    dp.add_handler(CommandHandler("load", load_account))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
