from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN: Final = [your telegram bot token]
BOT_USERNAME: Final = '@anti_huangniu_bot'

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("log.txt", "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line = file.readline().decode()
    await update.message.reply_text("ouch!🙄 " + last_line)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('kick', check_command))
    app.run_polling(poll_interval=3)