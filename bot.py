import os
from telegram import Update, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# متغيرات
TOKEN = os.environ.get("BOT_TOKEN")
users_data = {}  # تخزين بيانات المستخدمين: المحاولات والنجوم

# بيانات اختبار (يوزرات عشوائية صحيحة للتخمين)
correct_usernames = ["user123", "cool_guy", "test_hero"]

# عدد المحاولات الافتراضية
MAX_TRIES = 5

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users_data:
        users_data[user_id] = {"tries": MAX_TRIES, "stars": 0}

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="ابدأ التخمين",
            web_app=WebAppInfo(url="https://Telebot-user-guess-1.a75932020.repl.co")
        )
    ]])

    await update.message.reply_text("اضغط على الزر لبدء التخمين:", reply_markup=keyboard)

# استقبال التخمين
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    guess = update.message.text.strip()

    if user_id not in users_data:
        users_data[user_id] = {"tries": MAX_TRIES, "stars": 0}

    if users_data[user_id]["tries"] <= 0:
        await update.message.reply_text("خلصت محاولاتك! ادعُ صديق أو استنى لبكرة.")
        return

    if guess in correct_usernames:
        users_data[user_id]["stars"] += 1
        await update.message.reply_text(f"مبروك! التخمين صحيح.\nنجومك: {users_data[user_id]['stars']}")
    else:
        await update.message.reply_text("غلط! حاول تاني.")

    users_data[user_id]["tries"] -= 1
    await update.message.reply_text(f"المحاولات المتبقية: {users_data[user_id]['tries']}")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
