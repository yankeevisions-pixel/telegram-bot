
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 2006976532

NAME, PHONE, SERVICE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Как вас зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите ваш номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Какую услугу вы хотите получить?")
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["service"] = update.message.text

    text = (
        "Новая заявка:\n\n"
        f"Имя: {context.user_data['name']}\n"
        f"Телефон: {context.user_data['phone']}\n"
        f"Услуга: {context.user_data['service']}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    await update.message.reply_text("Спасибо! Мы скоро свяжемся с вами.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявка отменена.")
    return ConversationHandler.END

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

app.run_polling()
