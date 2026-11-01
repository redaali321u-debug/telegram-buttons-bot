import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

TABLES = {
    "table1": {
        "title": "الجدول الأول",
        "buttons": {
            "info1": "المعلومات الأولى",
            "info2": "المعلومات الثانية"
        }
    },
    "table2": {
        "title": "الجدول الثاني",
        "buttons": {
            "info3": "المعلومات الثالثة",
            "info4": "المعلومات الرابعة"
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("الجدول الأول", callback_data="table1"),
            InlineKeyboardButton("الجدول الثاني", callback_data="table2")
        ]
    ]

    await update.message.reply_text(
        "أهلاً بك في البوت\nاختر الجدول:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in TABLES:
        table = TABLES[query.data]
        keyboard = [
            [InlineKeyboardButton(name, callback_data=key)]
            for key, name in table["buttons"].items()
        ]
        keyboard.append([
            InlineKeyboardButton("رجوع للقائمة", callback_data="home")
        ])

        await query.edit_message_text(
            table["title"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "home":
        keyboard = [
            [
                InlineKeyboardButton("الجدول الأول", callback_data="table1"),
                InlineKeyboardButton("الجدول الثاني", callback_data="table2")
            ]
        ]
        await query.edit_message_text(
            "اختر الجدول:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:
        await query.message.reply_text(
            "سيتم إضافة المعلومات هنا قريباً."
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
