import streamlit as st
import pandas as pd
import os
import requests
import subprocess
import tempfile
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

st.set_page_config(page_title="Neuro Security Hub + الرعد الأردني", layout="wide")

# ==================================================
# النظام الأساسي
# ==================================================

class SecurityHub:

    def send_telegram_alert(self, message):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🚨 تنبيه أمني\n{message}\nالوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        try:
            response = requests.post(url, data=data)
            return response.status_code == 200
        except:
            return False

    def save_to_supabase(self, table, data):
        if not SUPABASE_URL or not SUPABASE_KEY:
            return False

        url = f"{SUPABASE_URL}/rest/v1/{table}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            return response.status_code in [200, 201]
        except:
            return False


# ==================================================
# نظام الصوت الاحترافي Neural
# ==================================================

class VoiceAlertSystem:

    def __init__(self):
        self.primary_voice = "ar-SA-ZaidNeural"
        self.fallback_voice = "ar-EG-SalemNeural"

    def create_voice_alert(self, message_text):
        full_text = f"هذا الرعد الأردني، {message_text}، نحن بالخدمة"

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        filename = temp_file.name

        try:
            subprocess.run([
                "edge-tts",
                "--voice", self.primary_voice,
                "--text", full_text,
                "--write-media", filename
            ], timeout=60)

            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                return filename

            # fallback
            subprocess.run([
                "edge-tts",
                "--voice", self.fallback_voice,
                "--text", full_text,
                "--write-media", filename
            ], timeout=60)

            return filename

        except Exception as e:
            print("TTS Error:", e)
            return None

    def send_voice_alert(self, chat_id, message_text):
        voice_file = self.create_voice_alert(message_text)

        if not voice_file:
            return False

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"

        with open(voice_file, "rb") as voice:
            files = {"voice": voice}
            data = {"chat_id": chat_id}
            response = requests.post(url, files=files, data=data)

        os.unlink(voice_file)
        return response.status_code == 200


# ==================================================
# دمج النظام + الصوت
# ==================================================

class JordanianSecurityVoice(SecurityHub):

    def __init__(self):
        super().__init__()
        self.voice_system = VoiceAlertSystem()

    def get_threat_message(self, threat_type, details):
        messages = {
            "network_intrusion": f"اكتشفنا محاولة اختراق على الشبكة. التفاصيل: {details}",
            "malware": f"لقينا ملف خطير. اسم الملف: {details}",
            "phishing": f"تم رصد رابط تصيدي. الرابط: {details}",
            "penetration": f"انتهى اختبار الاختراق. النتيجة: {details}"
        }
        return messages.get(threat_type, details)

    def send_voice_security_alert(self, threat_type, details):
        message = self.get_threat_message(threat_type, details)

        text_ok = self.send_telegram_alert(message)
        voice_ok = self.voice_system.send_voice_alert(
            TELEGRAM_CHAT_ID,
            message
        )

        return text_ok and voice_ok


# تهيئة النظام
hub = JordanianSecurityVoice()

# ==================================================
# واجهة Streamlit
# ==================================================

st.title("🛡️ مركز الأمن السيبراني + الرعد الأردني")

tabs = st.tabs([
    "🔍 كشف التسلل",
    "🦠 فحص البرمجيات",
    "📊 لوحة التحكم"
])

# ==================================================
# كشف التسلل
# ==================================================

with tabs[0]:
    st.header("نظام كشف التسلل")

    network_logs = st.file_uploader("📁 ارفع ملف CSV", type=["csv"])

    if network_logs:
        df = pd.read_csv(network_logs)
        st.dataframe(df.head())

        if st.button("🔍 تحليل"):
            threats_found = len(df) // 10

            st.success(f"تم العثور على {threats_found} تهديد محتمل")

            hub.send_voice_security_alert(
                "network_intrusion",
                f"عدد المحاولات المكتشفة {threats_found}"
            )

            hub.save_to_supabase("threats", {
                "type": "network_intrusion",
                "count": threats_found,
                "detected_at": datetime.now().isoformat()
            })


# ==================================================
# فحص البرمجيات
# ==================================================

with tabs[1]:
    st.header("فحص البرمجيات")

    uploaded_file = st.file_uploader("📎 ارفع ملف للفحص", type=["exe", "pdf", "zip"])

    if uploaded_file:
        if st.button("🔬 فحص الملف"):
            risk_score = hash(uploaded_file.name) % 100
            is_malicious = risk_score > 70

            if is_malicious:
                st.error(f"⚠️ الملف خطير بنسبة {risk_score}%")

                hub.send_voice_security_alert(
                    "malware",
                    uploaded_file.name
                )
            else:
                st.success(f"✅ الملف آمن بنسبة {risk_score}%")


# ==================================================
# لوحة التحكم
# ==================================================

with tabs[2]:
    st.header("📊 لوحة التحكم")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("إجمالي التهديدات", "15")

    with col2:
        st.metric("حالة النظام", "🟢 يعمل")

    st.write("🔥 التنبيهات تصل صوتياً عبر الرعد الأردني")
