import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== إعدادات البوت =====
BOT_TOKEN = os.environ.get("8765219444:AAGIRd-LACMU2JMC4difxksWywRZjUHFA80")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== قائمة السور مع file_id =====
# ضع file_id الخاص بكل سورة بعد رفع الملف الصوتي على تليقرام
SURAHS = [
    {"number": 1,   "name": "الفاتحة",       "file_id": ""},
    {"number": 2,   "name": "البقرة",         "file_id": ""},
    {"number": 3,   "name": "آل عمران",       "file_id": ""},
    {"number": 4,   "name": "النساء",         "file_id": ""},
    {"number": 5,   "name": "المائدة",        "file_id": ""},
    {"number": 6,   "name": "الأنعام",        "file_id": ""},
    {"number": 7,   "name": "الأعراف",        "file_id": ""},
    {"number": 8,   "name": "الأنفال",        "file_id": ""},
    {"number": 9,   "name": "التوبة",         "file_id": ""},
    {"number": 10,  "name": "يونس",           "file_id": ""},
    {"number": 11,  "name": "هود",            "file_id": ""},
    {"number": 12,  "name": "يوسف",           "file_id": ""},
    {"number": 13,  "name": "الرعد",          "file_id": ""},
    {"number": 14,  "name": "إبراهيم",        "file_id": ""},
    {"number": 15,  "name": "الحجر",          "file_id": ""},
    {"number": 16,  "name": "النحل",          "file_id": ""},
    {"number": 17,  "name": "الإسراء",        "file_id": ""},
    {"number": 18,  "name": "الكهف",          "file_id": ""},
    {"number": 19,  "name": "مريم",           "file_id": ""},
    {"number": 20,  "name": "طه",             "file_id": ""},
    {"number": 21,  "name": "الأنبياء",       "file_id": ""},
    {"number": 22,  "name": "الحج",           "file_id": ""},
    {"number": 23,  "name": "المؤمنون",       "file_id": ""},
    {"number": 24,  "name": "النور",          "file_id": ""},
    {"number": 25,  "name": "الفرقان",        "file_id": ""},
    {"number": 26,  "name": "الشعراء",        "file_id": ""},
    {"number": 27,  "name": "النمل",          "file_id": ""},
    {"number": 28,  "name": "القصص",          "file_id": ""},
    {"number": 29,  "name": "العنكبوت",       "file_id": ""},
    {"number": 30,  "name": "الروم",          "file_id": ""},
    {"number": 31,  "name": "لقمان",          "file_id": ""},
    {"number": 32,  "name": "السجدة",         "file_id": ""},
    {"number": 33,  "name": "الأحزاب",        "file_id": ""},
    {"number": 34,  "name": "سبأ",            "file_id": ""},
    {"number": 35,  "name": "فاطر",           "file_id": ""},
    {"number": 36,  "name": "يس",             "file_id": ""},
    {"number": 37,  "name": "الصافات",        "file_id": ""},
    {"number": 38,  "name": "ص",              "file_id": ""},
    {"number": 39,  "name": "الزمر",          "file_id": ""},
    {"number": 40,  "name": "غافر",           "file_id": ""},
    {"number": 41,  "name": "فصلت",           "file_id": ""},
    {"number": 42,  "name": "الشورى",         "file_id": ""},
    {"number": 43,  "name": "الزخرف",         "file_id": ""},
    {"number": 44,  "name": "الدخان",         "file_id": ""},
    {"number": 45,  "name": "الجاثية",        "file_id": ""},
    {"number": 46,  "name": "الأحقاف",        "file_id": ""},
    {"number": 47,  "name": "محمد",           "file_id": ""},
    {"number": 48,  "name": "الفتح",          "file_id": ""},
    {"number": 49,  "name": "الحجرات",        "file_id": ""},
    {"number": 50,  "name": "ق",              "file_id": ""},
    {"number": 51,  "name": "الذاريات",       "file_id": ""},
    {"number": 52,  "name": "الطور",          "file_id": ""},
    {"number": 53,  "name": "النجم",          "file_id": ""},
    {"number": 54,  "name": "القمر",          "file_id": ""},
    {"number": 55,  "name": "الرحمن",         "file_id": ""},
    {"number": 56,  "name": "الواقعة",        "file_id": ""},
    {"number": 57,  "name": "الحديد",         "file_id": ""},
    {"number": 58,  "name": "المجادلة",       "file_id": ""},
    {"number": 59,  "name": "الحشر",          "file_id": ""},
    {"number": 60,  "name": "الممتحنة",       "file_id": ""},
    {"number": 61,  "name": "الصف",           "file_id": ""},
    {"number": 62,  "name": "الجمعة",         "file_id": ""},
    {"number": 63,  "name": "المنافقون",      "file_id": ""},
    {"number": 64,  "name": "التغابن",        "file_id": ""},
    {"number": 65,  "name": "الطلاق",         "file_id": ""},
    {"number": 66,  "name": "التحريم",        "file_id": ""},
    {"number": 67,  "name": "الملك",          "file_id": ""},
    {"number": 68,  "name": "القلم",          "file_id": ""},
    {"number": 69,  "name": "الحاقة",         "file_id": ""},
    {"number": 70,  "name": "المعارج",        "file_id": ""},
    {"number": 71,  "name": "نوح",            "file_id": ""},
    {"number": 72,  "name": "الجن",           "file_id": ""},
    {"number": 73,  "name": "المزمل",         "file_id": ""},
    {"number": 74,  "name": "المدثر",         "file_id": ""},
    {"number": 75,  "name": "القيامة",        "file_id": ""},
    {"number": 76,  "name": "الإنسان",        "file_id": ""},
    {"number": 77,  "name": "المرسلات",       "file_id": ""},
    {"number": 78,  "name": "النبأ",          "file_id": ""},
    {"number": 79,  "name": "النازعات",       "file_id": ""},
    {"number": 80,  "name": "عبس",            "file_id": ""},
    {"number": 81,  "name": "التكوير",        "file_id": ""},
    {"number": 82,  "name": "الانفطار",       "file_id": ""},
    {"number": 83,  "name": "المطففين",       "file_id": ""},
    {"number": 84,  "name": "الانشقاق",       "file_id": ""},
    {"number": 85,  "name": "البروج",         "file_id": ""},
    {"number": 86,  "name": "الطارق",         "file_id": ""},
    {"number": 87,  "name": "الأعلى",         "file_id": ""},
    {"number": 88,  "name": "الغاشية",        "file_id": ""},
    {"number": 89,  "name": "الفجر",          "file_id": ""},
    {"number": 90,  "name": "البلد",          "file_id": ""},
    {"number": 91,  "name": "الشمس",          "file_id": ""},
    {"number": 92,  "name": "الليل",          "file_id": ""},
    {"number": 93,  "name": "الضحى",          "file_id": ""},
    {"number": 94,  "name": "الشرح",          "file_id": ""},
    {"number": 95,  "name": "التين",          "file_id": ""},
    {"number": 96,  "name": "العلق",          "file_id": ""},
    {"number": 97,  "name": "القدر",          "file_id": ""},
    {"number": 98,  "name": "البينة",         "file_id": ""},
    {"number": 99,  "name": "الزلزلة",        "file_id": ""},
    {"number": 100, "name": "العاديات",       "file_id": ""},
    {"number": 101, "name": "القارعة",        "file_id": ""},
    {"number": 102, "name": "التكاثر",        "file_id": ""},
    {"number": 103, "name": "العصر",          "file_id": ""},
    {"number": 104, "name": "الهمزة",         "file_id": ""},
    {"number": 105, "name": "الفيل",          "file_id": ""},
    {"number": 106, "name": "قريش",           "file_id": ""},
    {"number": 107, "name": "الماعون",        "file_id": ""},
    {"number": 108, "name": "الكوثر",         "file_id": ""},
    {"number": 109, "name": "الكافرون",       "file_id": ""},
    {"number": 110, "name": "النصر",          "file_id": ""},
    {"number": 111, "name": "المسد",          "file_id": ""},
    {"number": 112, "name": "الإخلاص",        "file_id": ""},
    {"number": 113, "name": "الفلق",          "file_id": ""},
    {"number": 114, "name": "الناس",          "file_id": ""},
]

SURAHS_PER_PAGE = 10  # عدد السور في كل صفحة


def build_keyboard(page: int) -> InlineKeyboardMarkup:
    """بناء لوحة الأزرار للصفحة المحددة"""
    start = page * SURAHS_PER_PAGE
    end = min(start + SURAHS_PER_PAGE, len(SURAHS))
    page_surahs = SURAHS[start:end]

    keyboard = []
    # أزرار السور (صفان بجانب بعض)
    for i in range(0, len(page_surahs), 2):
        row = []
        s = page_surahs[i]
        row.append(InlineKeyboardButton(
            f"{s['number']}. {s['name']}",
            callback_data=f"surah_{s['number']}"
        ))
        if i + 1 < len(page_surahs):
            s2 = page_surahs[i + 1]
            row.append(InlineKeyboardButton(
                f"{s2['number']}. {s2['name']}",
                callback_data=f"surah_{s2['number']}"
            ))
        keyboard.append(row)

    # أزرار التنقل بين الصفحات
    total_pages = (len(SURAHS) + SURAHS_PER_PAGE - 1) // SURAHS_PER_PAGE
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ السابق", callback_data=f"page_{page - 1}"))
    nav_row.append(InlineKeyboardButton(f"📖 {page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("التالي ▶️", callback_data=f"page_{page + 1}"))
    keyboard.append(nav_row)

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البدء /start"""
    await update.message.reply_text(
        "🌙 *بوت القرآن الكريم*\n\nاختر السورة التي تريد الاستماع إليها:",
        parse_mode="Markdown",
        reply_markup=build_keyboard(0)
    )


async def handle_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التنقل بين الصفحات"""
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await query.edit_message_text(
            "🌙 *بوت القرآن الكريم*\n\nاختر السورة التي تريد الاستماع إليها:",
            parse_mode="Markdown",
            reply_markup=build_keyboard(page)
        )
    elif data.startswith("surah_"):
        surah_num = int(data.split("_")[1])
        surah = next((s for s in SURAHS if s["number"] == surah_num), None)

        if not surah:
            await query.answer("⚠️ السورة غير موجودة!", show_alert=True)
            return

        if not surah["file_id"]:
            await query.answer("⚠️ الملف الصوتي لهذه السورة لم يُضف بعد.", show_alert=True)
            return

        await query.answer(f"⏳ جاري إرسال سورة {surah['name']}...")
        await context.bot.send_voice(
            chat_id=query.message.chat_id,
            voice=surah["file_id"],
            caption=f"🎙️ سورة *{surah['name']}* ({surah['number']})",
            parse_mode="Markdown"
        )
    elif data == "noop":
        await query.answer()


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_page))
    print("✅ البوت يعمل...")
    app.run_polling()


if __name__ == "__main__":
    main()
