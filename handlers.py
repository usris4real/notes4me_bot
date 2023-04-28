from telegram import Update
from telegram.ext import ContextTypes


# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a message with instructions on how to use this bot."""
    url = context.bot_data["url"]

    text = (
        '<b>Hello, glad to see you here.</b>\n\n'
        f"To check if the bot is still running, call <code>{url}/healthcheck</code>.\n\n"
    )

    await update.message.reply_html(text=text)
