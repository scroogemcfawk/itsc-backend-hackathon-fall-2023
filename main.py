import sqlite3

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Hello, {user.name}!"
    )


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    # Save user message in database
    cursor.executescript(f'''
    INSERT INTO Message (text) VALUES ("{text}")
    ''')
    # Save changes to database
    db.commit()
    await update.message.reply_text(
        "Your message has been saved!"
    )


if __name__ == "__main__":
    # Connect to database
    db = sqlite3.connect("database.db")

    cursor = db.cursor()

    # Create a table if it does not exist yet
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Message (
    id INTEGER PRIMARY KEY,
    text varchar(128)
    )
    ''')

    # Save changes in db
    db.commit()

    # Crate bot with token
    bot = Application.builder().token("6980628783:AAFaeqw1tV937ZYmDZxN6D_e8ip6vAth6h0").build()

    # Add message handlers to bot
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

    # Run bot
    bot.run_polling()

    # Close database connection
    db.close()
