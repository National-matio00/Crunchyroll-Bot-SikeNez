import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from time import time
from functools import wraps
from flask import Flask, request

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set your bot token and other variables
BOT_TOKEN = 'YOUR_BOT_TOKEN'
FORCE_SUB_CHANNEL = '@SikeNezCrunhy'  # Use the username, not the full URL
COOLDOWN = 7200  # 2 hours in seconds

accounts = []
user_cooldowns = {}
admins = [6043529845]  # Add your Telegram user ID as the initial admin

app = Flask(__name__)

# Check for forced subscription
def is_user_subscribed(user_id):
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

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Crunchyroll Account Bot!\n"
        "Use /GetCrunchyroll to claim an account.\n"
        "Only users subscribed to the channel can use this feature."
    )

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

# Webhook endpoint
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    updater.dispatcher.process_update(update)
    return 'ok'

def main():
    global updater
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("GetCrunchyroll", get_crunchyroll))
    dp.add_handler(CommandHandler("load", load_account))
    dp.add_handler(CommandHandler("addadmin", add_admin))

    # Set the webhook
    updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get('PORT', 5000)), url_path=BOT_TOKEN)
    updater.bot.set_webhook(f'https://your_render_app_url/{BOT_TOKEN}')  # Replace with your Render app URL

    updater.idle()

if __name__ == '__main__':
    main()
              
