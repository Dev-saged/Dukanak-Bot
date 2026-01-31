import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# --- 1. الإعدادات والأمان (Configuration) ---
# نقوم بتحميل التوكن من ملف .env لحماية البيانات
load_dotenv()
TOKEN = os.getenv("8482788521:AAGLSLYOoeZkgkFtu-m-qWs2hadJqfZGkRI")  # تأكد من وضع التوكن في ملف .env أو استبدله هنا مؤقتاً للتجربة

# تفعيل الـ Logging لمتابعة الأخطاء والأداء
logging.basicConfig(level=logging.INFO)

# تهيئة البوت والـ Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. الردود الجاهزة (Database of Responses) ---
# هنا نضع النصوص المتميزة التي صغناها سابقاً لتسهيل تعديلها لاحقاً
RESPONSES = {
    "welcome": (
        "<b>أهلاً وسهلاً فيك في عالم دُكانك، ويسعدنا تواصلك معنا 🌹</b>\n\n"
        "دُكانك هو منصتك المتكاملة للبيع والشراء في غزة. "
        "نربطك مباشرة بالتاجر أو الزبون، مع خدمة توصيل سريعة عبر 'دليفري برق'.\n\n"
        "🚀 <b>الانطلاق الرسمي:</b> خلال أقل من 5 أيام إن شاء الله!\n\n"
        "كيف يمكنني مساعدتك اليوم؟ اختر من الأسفل 👇"
    ),
    "link": (
        "<b>أهلاً وسهلاً فيك في عالم دُكانك 🌹</b>\n\n"
        "إحنا حالياً في مرحلة العد التنازلي! ⏳\n"
        "روابط التحميل ستكون متاحة خلال <b>أقل من 5 أيام</b> على Google Play و App Store.\n\n"
        "تابعنا هنا ليصلك الإشعار فوراً:"
    ),
    "how_it_works": (
        "<b>أهلاً وسهلاً فيك في عالم دُكانك 🌹</b>\n\n"
        "الفكرة بسيطة وتوفر عليك الكثير:\n"
        "1️⃣ <b>للبيع:</b> صور منتجك (جديد أو مستعمل)، حدد السعر، واحنا بنعرضه.\n"
        "2️⃣ <b>للشراء:</b> اطلب من بيتك بنفس سعر السوق.\n"
        "3️⃣ <b>التوصيل:</b> سريع ومضمون لكل مناطق القطاع.\n\n"
        "وفر وقتك ومواصلاتك مع دُكانك! 🚀"
    ),
    "support": (
        "<b>خدمة العملاء 🌹</b>\n\n"
        "يمكنك ترك رسالتك هنا وسيقوم أحد موظفينا بالرد عليك في أقرب وقت.\n"
        "نحن هنا لخدمتكم!"
    )
}

# --- 3. لوحات المفاتيح (Keyboards & UI) ---
# تصميم كيبورد تفاعلي يظهر تحت الرسالة
def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 رابط التحميل", callback_data="btn_link"),
            InlineKeyboardButton(text="💡 كيف يعمل؟", callback_data="btn_how")
        ],
        [
            InlineKeyboardButton(text="📞 تواصل معنا", callback_data="btn_support"),
            InlineKeyboardButton(text="🌐 صفحاتنا", url="https://your-social-link.com") # ضع رابط صفحاتكم الموحد هنا
        ]
    ])
    return keyboard

# --- 4. معالجة الأحداث (Handlers & Logic) ---

# أ. معالجة أمر البداية /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        text=RESPONSES["welcome"],
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu()
    )

# ب. معالجة الضغط على الأزرار (Callbacks)
@dp.callback_query()
async def callbacks_handler(callback: types.CallbackQuery):
    # تحليل الزر المضغوط
    if callback.data == "btn_link":
        await callback.message.answer(RESPONSES["link"], parse_mode=ParseMode.HTML)
    elif callback.data == "btn_how":
        await callback.message.answer(RESPONSES["how_it_works"], parse_mode=ParseMode.HTML)
    elif callback.data == "btn_support":
        await callback.message.answer(RESPONSES["support"], parse_mode=ParseMode.HTML)
    
    # إغلاق حالة التحميل للزر (ليتوقف عن الدوران)
    await callback.answer()

# ج. الذكاء في تحليل النصوص (AI-like Keyword Matching)
# هذا الجزء يستمع لأي نص يكتبه المستخدم ويحاول فهمه
@dp.message(F.text)
async def smart_reply(message: types.Message):
    user_text = message.text.lower() # تحويل النص لأحرف صغيرة لتسهيل البحث (مفيد للانجليزي أكثر)
    
    # تحليل الكلمات المفتاحية
    if any(word in user_text for word in ["رابط", "تحميل", "نزل", "لينك", "متجر"]):
        await message.reply(RESPONSES["link"], parse_mode=ParseMode.HTML)
        
    elif any(word in user_text for word in ["تفاصيل", "فكرة", "شرح", "كيف", "آلية"]):
        await message.reply(RESPONSES["how_it_works"], parse_mode=ParseMode.HTML)
        
    elif any(word in user_text for word in ["مرحبا", "هلا", "سلام", "مساء"]):
        await message.reply(RESPONSES["welcome"], parse_mode=ParseMode.HTML, reply_markup=get_main_menu())
        
    else:
        # الرد الافتراضي في حال لم يفهم البوت السؤال
        # يمكن هنا ربطه مستقبلاً بـ ChatGPT API
        await message.reply(
            "وصلتنا رسالتك 🌹\n"
            "سؤالك مهم، وسيتم تحويله لفريق الدعم للرد عليك بدقة.\n"
            "وفي الأثناء، يمكنك الاطلاع على القائمة أدناه:",
            reply_markup=get_main_menu()
        )

# --- 5. تشغيل البوت (Main Execution) ---
async def main():
    print("Bot is starting...")
    # حذف الـ Webhook القديم لضمان عمل الـ Polling بسلاسة
    await bot.delete_webhook(drop_pending_updates=True)
    # البدء في الاستماع
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
