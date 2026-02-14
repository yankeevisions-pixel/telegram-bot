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

# ВСТАВЬ СЮДА СВОЙ TELEGRAM ID
ADMIN_ID = 2006976532  

NAME, PHONE, SERVICE = range(3)


# --- СТАРТ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚗 Привет! Нужны автозапчасти?\n\n"
        "Поможем подобрать быстро и без лишней головной боли 👍\n"
        "Как вас зовут?"
    )
    return NAME


# --- ПОЛУЧАЕМ ИМЯ ---
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите ваш номер телефона:")
    return PHONE


# --- ПОЛУЧАЕМ ТЕЛЕФОН ---
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Что именно вам нужно? Опишите деталь:")
    return SERVICE


# --- ПОЛУЧАЕМ ЗАЯВКУ ---
async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["service"] = update.message.text

    name = context.user_data["name"]
    phone = context.user_data["phone"]
    service = context.user_data["service"]

    text = (
        f"📩 Новая заявка!\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"🔧 Запрос: {service}"
    )

    # Отправляем админу
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    await update.message.reply_text(
        "✅ Спасибо! Ваша заявка принята.\n"
        "Мы свяжемся с вами в ближайшее время."
    )

    return ConversationHandler.END


# --- ОТМЕНА ---
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Заявка отменена.")
    return ConversationHandler.END


def main():
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


if __name__ == "__main__":
    main()


