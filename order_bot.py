from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, time
import pytz
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = int(os.environ.get('ADMIN_CHAT_ID'))
tz = pytz.timezone('Europe/Rome')

def is_within_working_hours():
    now = datetime.now(tz).time()
    return time(10, 0) <= now <= time(22, 30)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напишите свой заказ здесь.")

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_within_working_hours():
        await update.message.reply_text("Приём заказов с 10:00 до 22:30. Напишите позже — мы обязательно ответим!")
        return

    user = update.message.from_user
    order_text = update.message.text
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Новый заказ от @{user.username or user.first_name}:

{order_text}")
    await update.message.reply_text("Спасибо! Ваш заказ отправлен.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order))
app.run_polling()
