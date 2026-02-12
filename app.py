import streamlit as st
import pandas as pd
import os
import requests
import json
import tempfile
from datetime import datetime
from dotenv import load_dotenv
from gtts import gTTS
from groq import Groq
from tavily import TavilyClient

# --- 1. إعدادات البيئة والهوية ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GROQ_API_KEY = os.getenv('GROK_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

st.set_page_config(page_title="Thunder Security Hub Pro", layout="wide")

# --- 2. نظام التنبيه الصوتي الأردني (VoiceAlertSystem) ---
class VoiceAlertSystem:
    def __init__(self):
        self.bot_name = "الرعد الاردني"
        self.voice_lang = 'ar'
        self.voice_tld = 'com.au' # نبرة قد تميل للرجولية أكثر في التردد
        
    def add_jordanian_dialect(self, text):
        """تحويل النص إلى نبرة أردنية استخباراتية"""
        jordanian_text = text.replace("تم الكشف", "اكتشفنا").replace("ملف خبيث", "ملف خطيير").replace("اختراق", "اخترااق")
        intro = "هذا الرعد الاردني، "
        outro = "، نحن بالخدمة يا قائد."
        return intro + jordanian_text + outro

    def create_voice_alert(self, message_text):
        jordanian_message = self.add_jordanian_dialect(message_text)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        filename = temp_file.name
        tts = gTTS(text=jordanian_message, lang=self.voice_lang, slow=False)
        tts.save(filename)
        return filename

    def send_voice_alert(self, chat_id, message_text):
        voice_file = self.create_voice_alert(message_text)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
        try:
            with open(voice_file, 'rb') as voice:
                requests.post(url, files={'voice': voice}, data={'chat_id': chat_id})
            os.unlink(voice_file)
            return True
        except: return False

# --- 3. المركز الأمني المطور (Security Engine) ---
class SecurityHub:
    def send_telegram_alert(self, message):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": f"🚨 {message}"}
        requests.post(url, data=data)

class JordanianSecurityVoice(SecurityHub):
    def __init__(self):
        self.voice_system = VoiceAlertSystem()
        
    def send_jordanian_voice_alert(self, message):
        self.send_telegram_alert(message) # إرسال نص
        return self.voice_system.send_voice_alert(TELEGRAM_CHAT_ID, message) # إرسال صوت

    def get_jordanian_threat_message(self, threat_type, details):
        messages = {
            "network_intrusion": f"تحذير! اكتشفنا محاولة اختراق على الشبكة. التفاصيل: {details}",
            "malware": f"الرعد يحذر! لقينا ملف خطيير. اسمه: {details}",
            "phishing": f"نبهناك! هذا رابط تصيدي. الرابط: {details}",
            "penetration": f"خلصنا اختبار الاختراق. النتيجة: {details}"
        }
        return messages.get(threat_type, f"تنبيه أمني: {details}")

# تهيئة الرعد الأردني الناطق
hub = JordanianSecurityVoice()

# --- 4. واجهة المستخدم (Streamlit Interface) ---
st.title("🛡️ مركز الرعد الأردني للأمن السيبراني")
tabs = st.tabs(["🔍 كشف التسلل", "🦠 البرمجيات الخبيثة", "🎣 مكافحة التصيد", "⚔️ اختبار الاختراق", "📊 لوحة التحكم"])

# مثال: وحدة كشف التسلل (المنطق المدمج)
with tabs[0]:
    st.header("كشف التسلل بالذكاء الاصطناعي")
    network_logs = st.file_uploader("📁 ارفع سجلات الشبكة", type=['csv', 'txt'])
    if network_logs:
        if st.button("🔍 تحليل الرعد"):
            with st.spinner("جاري الرصد..."):
                # محاكاة تحليل
                msg = hub.get_jordanian_threat_message("network_intrusion", "محاولة دخول من IP خارجي")
                hub.send_jordanian_voice_alert(msg)
                st.success("تم إرسال التنبيه النصي والصوتي للأجهزة المرتبطة.")

# وحدة البرمجيات الخبيثة
with tabs[1]:
    st.header("محلل البرمجيات الخبيثة")
    up_file = st.file_uploader("📎 فحص ملف مشبوه", type=['exe', 'pdf', 'zip'])
    if up_file:
        if st.button("🔬 فحص"):
            msg = hub.get_jordanian_threat_message("malware", up_file.name)
            hub.send_jordanian_voice_alert(msg)
            st.error("⚠️ ملف مشبوه! تم إرسال البلاغ الصوتي.")

# وحدة مكافحة التصيد
with tabs[2]:
    url_input = st.text_input("🔗 فحص رابط:")
    if url_input and st.button("🛡️ فحص"):
        msg = hub.get_jordanian_threat_message("phishing", url_input)
        hub.send_jordanian_voice_alert(msg)
        st.warning("تم إخطار مركز العمليات بالرابط المشبوه.")

# الجانب الإحصائي
with tabs[4]:
    st.metric("حالة النظام الصوتي", "نشط 🎙️", delta="أردني")
    st.info("النظام يقوم بتحويل التنبيهات إلى بصمات صوتية (MP3) وإرسالها لتلغرام فوراً.")
