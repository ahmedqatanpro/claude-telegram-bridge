import os
import telebot
from telebot.types import Message

# جلب المفاتيح من بيئة الاستضافة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# تهيئة البوت
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("خطأ أمني: لم يتم العثور على TELEGRAM_BOT_TOKEN في متغيرات البيئة.")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ---------------------------------------------------------
# طبقة الحماية (Security & Auth Layer)
# ---------------------------------------------------------
AUTHENTICATED_USERS = set()
BOT_PASSWORD = "779460213"

def is_authenticated(user_id: int) -> bool:
    return user_id in AUTHENTICATED_USERS

# ---------------------------------------------------------
# محرك معالجة الرسائل (Message Handler)
# ---------------------------------------------------------
@bot.message_handler(func=lambda message: True)
def handle_incoming_messages(message: Message):
    user_id = message.chat.id
    user_text = message.text.strip()

    # 1. التحقق من الصلاحيات أولاً (Authentication Check)
    if not is_authenticated(user_id):
        if user_text == BOT_PASSWORD:
            AUTHENTICATED_USERS.add(user_id)
            bot.reply_to(message, "تم توثيق الدخول بنجاح. النظام جاهز لتلقي الأوامر البرمجية والتحليل.")
        else:
            bot.reply_to(message, "نعم أهلاً بك، أنا روبرت بنيان للبرمجيات. أرسل كلمة المرور لكي تتمكن من استخدامي بحرية.")
        return # إيقاف التنفيذ هنا لمنع غير المصرح لهم من استهلاك الموارد

    # 2. توجيه الأوامر للوكيل (Proxy Routing)
    # هذا القسم يتم تفعيله فقط للمستخدمين الموثقين
    try:
        # رسالة مؤقتة لتأكيد الاستلام
        processing_msg = bot.reply_to(message, "⚙️ جاري تحليل الأمر وتوجيهه للوكيل...")
        
        # [ملاحظة معمارية]: هنا يتم استدعاء دالة free-claude-code الأصلية
        # process_with_claude(user_text)
        
        # محاكاة لرد الوكيل (يُستبدل بالرد الفعلي من Claude/OpenRouter)
        bot.edit_message_text(
            chat_id=user_id,
            message_id=processing_msg.message_id,
            text=f"تم تنفيذ الأمر: {user_text}\n(هذا الرد قادم من بيئة الوكيل المحمية)"
        )
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ في خادم الوكيل: {str(e)}")

# ---------------------------------------------------------
# نقطة الإطلاق (Entry Point)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("تم تفعيل نظام روبرت بنيان للبرمجيات.")
    print("طبقة الحماية: نشطة.")
    print("البوت الآن في وضع الاستماع المستمر...")
    
    # تشغيل البوت متجاهلاً الأخطاء المؤقتة للشبكة لضمان الاستمرارية
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
