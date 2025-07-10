import os
from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, ConversationHandler, filters
)

TOKEN = os.getenv("BOT_TOKEN") or "توکن_ربات_تو_اینجا_بزار"
CHANNEL = "@ogabnet"
ADMIN_ID = 7400790423
CONFIG_FILE = "configs/config_1day.txt"
WAITING_CONFIG_TEXT = 1

# --- کیبورد‌ها ---
start_keyboard = [["✅ چک عضویت در کانال", "📢 ورود به کانال"]]
main_menu_keyboard = [
    ["🧩 سرویس ها و اشتراک های من 🧩"],
    ["🛍️💳 کیف پول/موجودی من 💳🛍️"],
    ["☎️ پشتیبانی 24 ساعته سریع و الصیف ☎️"],
    ["🥇 خرید اشتراک اختصاصی 🥇"],
    ["📌 سوالات متداول 📌"],
    ["💱♻️ تمدید سرویس‌ها ♻️💱"],
    ["🚀💲💱 دریافت کانفیگ تست 💱💲🚀"],
]
faq_keyboard = [
    ["نحوه اتصال در اندروید"],
    ["نحوه اتصال در آیفون"],
    ["نحوه اتصال در کامپیوتر"],
    ["🔙 بازگشت به منو"],
]
wallet_keyboard = [
    ["💶💵 افزایش موجودی 💵💶", "💰💰 کیف پول/موجودی من 💰💰"],
    ["🔙 بازگشت به منو"],
]
subs_keyboard = [
    ["🇲🇽 Tگیگ25 تک کاربر 100 🎖️"],
    ["🇬🇷 Tگیگ35 دو کاربر 135 🥇"],
    ["🇫🇮 Tگیگ50 سه کاربر 165 👑"],
    ["🇹🇷 Tگیگ100 پنج کاربر 250 ☢️"],
    ["🔙 بازگشت به منو"],
]


# --- استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True),
    )


# --- چک عضویت ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        if member.status in ["member", "creator", "administrator"]:
            await update.message.reply_text(
                "🎉 تبریک! شما عضو کانال هستید.",
                reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True),
            )
        else:
            await update.message.reply_text(
                f"❌ شما عضو کانال {CHANNEL} نیستید!\n"
                "لطفاً ابتدا به کانال بپیوندید و سپس دوباره تلاش کنید.",
                reply_markup=ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True),
            )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا در بررسی عضویت: {e}")


# --- پیام‌ها ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id == ADMIN_ID and context.user_data.get("waiting_for_config_text"):
        await send_custom_message_to_user(update, context, text)
        return

    if text == "✅ چک عضویت در کانال":
        await check_membership(update, context)
    elif text == "📢 ورود به کانال":
        await update.message.reply_text(f"لینک کانال:\n{CHANNEL}")
    elif text == "🧩 سرویس ها و اشتراک های من 🧩":
        await update.message.reply_text("💡 شما هیچ اشتراکی از عقاب نت تهیه نکردید 💡")
    elif text == "🛍️💳 کیف پول/موجودی من 💳🛍️":
        await update.message.reply_text("🛍️ کیف پول شما 🛍️", reply_markup=ReplyKeyboardMarkup(wallet_keyboard, resize_keyboard=True))
    elif text == "💰💰 کیف پول/موجودی من 💰💰":
        await update.message.reply_text(f"🆔 شناسه عددی: {user_id}\n🗃 کل سرویس‌ها: 0 عدد 📚\n💵 موجودی کیف پول: 0 تومان 💵")
    elif text == "💶💵 افزایش موجودی 💵💶":
        await update.message.reply_text("6219861991474080 بانو زهرا قربانی\n📩 لطفاً تصویر رسید را همینجا ارسال نمایید👇")
    elif text == "☎️ پشتیبانی 24 ساعته سریع و الصیف ☎️":
        await update.message.reply_text("@Ogabneting  تلگرام\n@Ogabnet       روبیکا")
    elif text == "🥇 خرید اشتراک اختصاصی 🥇":
        await update.message.reply_text("🥇 اشتراک را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(subs_keyboard, resize_keyboard=True))
    elif text in [btn[0] for btn in subs_keyboard[:-1]]:
        price_map = {
            "🇲🇽 Tگیگ25 تک کاربر 100 🎖️": "100 هزار تومان",
            "🇬🇷 Tگیگ35 دو کاربر 135 🥇": "135 هزار تومان",
            "🇫🇮 Tگیگ50 سه کاربر 165 👑": "165 هزار تومان",
            "🇹🇷 Tگیگ100 پنج کاربر 250 ☢️": "250 هزار تومان",
        }
        await update.message.reply_text(
            f"شماره کارت: 6219861991474080 خانوم قربانی\n"
            f"📩 لطفاً تصویر رسید را همینجا ارسال نمایید\n"
            f"مبلغ: {price_map.get(text, 'نامشخص')}"
        )
    elif text == "📌 سوالات متداول 📌":
        await update.message.reply_text("لطفاً موضوع مورد نظر را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(faq_keyboard, resize_keyboard=True))
    elif text in [row[0] for row in faq_keyboard[:-1]]:
        faq_answers = {
            "نحوه اتصال در اندروید": "برنامه رو نصب کن و کانفیگ وارد کن.",
            "نحوه اتصال در آیفون": "در تنظیمات VPN، کانفیگ رو وارد کن.",
            "نحوه اتصال در کامپیوتر": "نرم‌افزار رو نصب و لاگین کن.",
        }
        await update.message.reply_text(faq_answers.get(text, "اطلاعاتی نیست"))
    elif text == "💱♻️ تمدید سرویس‌ها ♻️💱":
        await update.message.reply_text("❗ هنوز سرویسی خریداری نکرده‌اید.")
    elif text == "🚀💲💱 دریافت کانفیگ تست 💱💲🚀":
        try:
            with open(CONFIG_FILE, "r") as f:
                config = f.read()
            await update.message.reply_text(f"🔓 کانفیگ تست یک‌روزه:\n\n{config}")
        except Exception as e:
            await update.message.reply_text(f"❌ فایل کانفیگ پیدا نشد: {e}")
    elif text == "🔙 بازگشت به منو":
        await update.message.reply_text("🧩 منوی اصلی عقاب نت 🧩", reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True))
    else:
        await update.message.reply_text("لطفاً از دکمه‌ها استفاده کنید.")


# --- رسید عکس ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    file_id = update.message.photo[-1].file_id
    caption = (
        f"📥 رسید پرداخت از:\n"
        f"👤 {user.full_name}\n"
        f"🆔 {user.id}\n"
        f"📛 @{user.username or 'ندارد'}\n\n"
        "برای ارسال کانفیگ، روی دکمه زیر بزن:"
    )
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚀 ارسال کانفیگ", callback_data=f"sendcfg_{user.id}")]]
    )
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=file_id, caption=caption, reply_markup=keyboard)
    await update.message.reply_text("رسید دریافت شد. به‌زودی کانفیگ ارسال می‌شود.")


# --- ارسال کانفیگ سفارشی توسط ادمین ---
async def send_custom_message_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    user_id = context.user_data.get("sendcfg_user_id")
    if not user_id:
        await update.message.reply_text("❌ شناسه کاربر یافت نشد.")
        context.user_data.clear()
        return
    try:
        await context.bot.send_message(chat_id=user_id, text=text)
        await update.message.reply_text("✅ کانفیگ ارسال شد.", reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True))
    except Exception as e:
        await update.message.reply_text(f"❌ خطا در ارسال پیام: {e}")
    context.user_data.clear()


# --- کلیک روی "ارسال کانفیگ" ---
async def send_config_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        await query.reply_text("❌ شما مجوز ندارید.")
        return
    _, user_id_str = query.data.split("_", maxsplit=1)
    user_id = int(user_id_str)
    context.user_data["sendcfg_user_id"] = user_id
    context.user_data["waiting_for_config_text"] = True
    await query.message.reply_text("متن کانفیگ را ارسال کن یا 'انصراف' بزن.", reply_markup=ReplyKeyboardMarkup([["انصراف"]], resize_keyboard=True))


# --- انصراف ---
async def cancel_config_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "انصراف":
        context.user_data.clear()
        await update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True))


# --- اجرای اصلی ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(send_config_callback, pattern=r"^sendcfg_\d+$")],
        states={
            WAITING_CONFIG_TEXT: [
                MessageHandler(filters.Regex("^انصراف$"), cancel_config_input),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ]
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(conv_handler)

    print("✅ ربات فعال شد.")
    app.run_polling()
