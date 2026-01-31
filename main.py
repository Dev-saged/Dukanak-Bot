import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiohttp import web  # لإنشاء سيرفر وهمي يرضي Render

# --- 1. إعدادات البوت والتوكن ---
# لقد قمت بوضع التوكن الخاص بك هنا مباشرة
TOKEN = "8482788521:AAGLSLYOoeZkgkFtu-m-qWs2hadJqfZGkRI"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. الردود الجاهزة ---
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

# --- 3. لوحات المفاتيح ---
def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 رابط التحميل", callback_data="btn_link"),
            InlineKeyboardButton(text="💡 كيف يعمل؟", callback_data="btn_how")
        ],
        [
            InlineKeyboardButton(text="📞 تواصل معنا", callback_data="btn_support"),
            InlineKeyboardButton(text="🌐 صفحاتنا", url="https://your-social-link.com")
        ]
    ])
    return keyboard

# --- 4. معالجة الرسائل والأزرار ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        text=RESPONSES["welcome"],
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu()
    )

@dp.callback_query()
async def callbacks_handler(callback: types.CallbackQuery):
    if callback.data == "btn_link":
        await callback.message.answer(RESPONSES["link"], parse_mode=ParseMode.HTML)
    elif callback.data == "btn_how":
        await callback.message.answer(RESPONSES["how_it_works"], parse_mode=ParseMode.HTML)
    elif callback.data == "btn_support":
        await callback.message.answer(RESPONSES["support"], parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.message(F.text)
async def smart_reply(message: types.Message):
    user_text = message.text.lower()
    if any(word in user_text for word in ["رابط", "تحميل", "نزل", "لينك", "متجر"]):
        await message.reply(RESPONSES["link"], parse_mode=ParseMode.HTML)
    elif any(word in user_text for word in ["تفاصيل", "فكرة", "شرح", "كيف", "آلية"]):
        await message.reply(RESPONSES["how_it_works"], parse_mode=ParseMode.HTML)
    elif any(word in user_text for word in ["مرحبا", "هلا", "سلام", "مساء"]):
        await message.reply(RESPONSES["welcome"], parse_mode=ParseMode.HTML, reply_markup=get_main_menu())
    else:
        await message.reply(
            "وصلتنا رسالتك 🌹\n"
            "سؤالك مهم، وسيتم تحويله لفريق الدعم للرد عليك بدقة.\n"
            "وفي الأثناء، يمكنك الاطلاع على القائمة أدناه:",
            reply_markup=get_main_menu()
        )

# --- 5. سيرفر وهمي (Dummy Server) لحل مشكلة البورت في Render ---
async def health_check(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render يعطي البورت في المتغير PORT، إذا لم يجده يستخدم 8080
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# --- 6. التشغيل الرئيسي ---
async def main():
    # تشغيل السيرفر الوهمي
    await start_web_server()
    
    print("Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # إضافة os هنا لأنه مستخدم في دالة البورت
    import os 
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
