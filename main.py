import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.enums import ParseMode
from aiohttp import web

# --- 1. إعدادات المشروع (Configuration) ---

# التوكين الجديد الخاص بك
TOKEN = "8482788521:AAGwjUpUjNlb9Vdp4fZZpKnUQqugYGcrSYQ"

# الرابط الموحد (Linktree)
LINKTREE_URL = "https://linktr.ee/dukanakworld1?utm_source=linktree_profile_share"

# تفعيل تسجيل الأحداث (Logging) لمراقبة البوت
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تهيئة البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. قاعدة بيانات الردود الذكية (Smart Responses) ---
# تم صياغة الردود لتكون فخمة، مرحبة، وتعكس هوية "دُكانك"

RESPONSES = {
    "welcome": (
        "<b>أهلاً وسهلاً بك في عالم دُكانك 🛍️</b>\n\n"
        "نورتنا! دُكانك هو التطبيق الأول في غزة الذي يجمع التاجر والزبون في مكان واحد.\n"
        "🚚 <b>توصيل سريع:</b> بالتعاون مع دليفري برق.\n"
        "💰 <b>بيع واشترِ:</b> جديد أو مستعمل، بخصوصية تامة.\n"
        "⏳ <b>الانطلاق الرسمي:</b> خلال أقل من 5 أيام إن شاء الله!\n\n"
        "كيف يمكننا خدمتك اليوم؟ اختر من القائمة:"
    ),
    "link": (
        "<b>📥 روابط تحميل دُكانك والمتابعة</b>\n\n"
        "إحنا حالياً في مرحلة العد التنازلي! التطبيق سينطلق خلال <b>أقل من 5 أيام</b> على Google Play و App Store.\n\n"
        "🔗 <b>تابعنا واحصل على الرابط فور صدوره من هنا:</b>\n"
        f"{LINKTREE_URL}\n\n"
        "خليك قريب، المفاجآت جاية! 🚀"
    ),
    "details": (
        "<b>💡 كيف يعمل دُكانك؟</b>\n\n"
        "فكرتنا بسيطة لتسهل حياتك وتوفر وقتك ومواصلاتك:\n\n"
        "1️⃣ <b>للبيع:</b> عندك غرض؟ صوره، حط سعره، واحنا بنعرضه للآلاف.\n"
        "2️⃣ <b>للشراء:</b> تصفح واطلب وأنت في بيتك بنفس سعر السوق.\n"
        "3️⃣ <b>التوصيل:</b> يوصلك طلبك وين ما كنت في القطاع.\n\n"
        "دُكانك.. سوقك في جيبك! 📱"
    ),
    "support": (
        "<b>📞 خدمة العملاء</b>\n\n"
        "نحن هنا لسماعك! يمكنك مراسلتنا هنا وسيتم الرد عليك من قبل الفريق المختص بأسرع وقت.\n"
        "رضاكم هو هدفنا 🌹"
    )
}

# --- 3. تصميم القوائم (Keyboards) ---

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 روابط التحميل وصفحاتنا", url=LINKTREE_URL)
        ],
        [
            InlineKeyboardButton(text="💡 كيف يعمل التطبيق؟", callback_data="btn_how"),
            InlineKeyboardButton(text="📞 تواصل معنا", callback_data="btn_support")
        ]
    ])
    return keyboard

# --- 4. معالجة الأوامر والرسائل (Handlers) ---

# أ. عند الضغط على start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    logger.info(f"New user started the bot: {message.from_user.id}")
    await message.answer(
        text=RESPONSES["welcome"],
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu()
    )

# ب. عند الضغط على الأزرار الداخلية
@dp.callback_query()
async def callbacks_handler(callback: types.CallbackQuery):
    action = callback.data
    logger.info(f"User clicked button: {action}")
    
    if action == "btn_how":
        await callback.message.answer(RESPONSES["details"], parse_mode=ParseMode.HTML)
    elif action == "btn_support":
        await callback.message.answer(RESPONSES["support"], parse_mode=ParseMode.HTML)
    
    await callback.answer()

# ج. الرد الذكي (تحليل النصوص)
@dp.message(F.text)
async def smart_analyzer(message: types.Message):
    text = message.text.lower()
    logger.info(f"Received message: {text}")

    # تحليل الكلمات المفتاحية
    if any(word in text for word in ["رابط", "لينك", "تحميل", "تنزيل", "متجر", "ايفون", "اندرويد"]):
        await message.reply(RESPONSES["link"], parse_mode=ParseMode.HTML)
        
    elif any(word in text for word in ["كيف", "شرح", "تفاصيل", "آلية", "فكرة", "معلومات"]):
        await message.reply(RESPONSES["details"], parse_mode=ParseMode.HTML)
        
    elif any(word in text for word in ["مرحبا", "هلا", "سلام", "مساء", "صباح"]):
        await message.reply(RESPONSES["welcome"], parse_mode=ParseMode.HTML, reply_markup=get_main_menu())
        
    else:
        # الرد الافتراضي إذا لم يفهم البوت
        await message.reply(
            "وصلت رسالتك 🌹\n"
            "سؤالك مهم، وسيتم الرد عليك بدقة قريباً.\n"
            "وفي الأثناء، يمكنك الاطلاع على الروابط والتفاصيل من هنا:",
            reply_markup=get_main_menu()
        )

# --- 5. إعدادات السيرفر (لضمان عمل البوت على Render) ---

async def health_check(request):
    return web.Response(text="Dukanak Bot is Alive & Running! 🚀")

async def start_web_server():
    # إنشاء تطبيق ويب بسيط
    app = web.Application()
    app.router.add_get('/', health_check)
    
    # تجهيز المشغل
    runner = web.AppRunner(app)
    await runner.setup()
    
    # الحصول على البورت من متغيرات البيئة (Render يفرضه) أو استخدام 8080
    port = int(os.environ.get("PORT", 8080))
    
    # تشغيل الموقع
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Web server started on port {port}")

# --- 6. التشغيل الرئيسي ---

async def main():
    # 1. تشغيل السيرفر الوهمي (لإبقاء Render سعيداً)
    await start_web_server()
    
    # 2. حذف الـ Webhook القديم وتنظيف التحديثات المعلقة
    logger.info("Cleaning updates and starting polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    # 3. بدء الاستماع للرسائل
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
