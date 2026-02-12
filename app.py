import streamlit as st
import pandas as pd
import os
import requests
import json
import tempfile
import socket
from datetime import datetime
from dotenv import load_dotenv
from gtts import gTTS
# استيراد هادئ لـ Scapy لتجنب الانهيار عند البدء
try:
    from scapy.all import IP, TCP, send
    SCAPY_AVAILABLE = True
except:
    SCAPY_AVAILABLE = False

# --- 1. إعدادات الهوية والترسانة ---
load_dotenv()
# جلب المفاتيح من Secrets (للسحاب) أو البيئة المحلية
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN") or os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID") or os.getenv('TELEGRAM_CHAT_ID')

st.set_page_config(page_title="Thunder Offensive Hub", layout="wide")

# --- 2. محرك العمليات الهجومية (The Offensive Engine) ---
class OffensiveModule:
    @staticmethod
    def port_scanner(target_ip, ports):
        """ فحص المنافذ باستخدام Socket (آمن ويعمل في السحاب) """
        open_ports = []
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((target_ip, port)) == 0:
                    open_ports.append(port)
                s.close()
            except: continue
        return open_ports

    @staticmethod
    def packet_crafter(target_ip):
        """ صناعة حزم مع نظام حماية من الانهيار """
        if not SCAPY_AVAILABLE:
            return "ERROR", "مكتبة Scapy غير متوفرة أو معطلة في هذه البيئة."
        
        try:
            # بناء حزمة SYN
            packet = IP(dst=target_ip)/TCP(dport=80, flags="S")
            # محاولة الإرسال - ستفشل في السحاب وتعطي PermissionError
            send(packet, verbose=False)
            return "SUCCESS", "تم إرسال حزمة (Crafted Packet) بنجاح."
        except PermissionError:
            return "PERMISSION_ERROR", "السيرفر السحابي يمنع إرسال حزم Raw (نقص صلاحيات Root)."
        except Exception as e:
            return "ERROR", f"خطأ تقني: {str(e)}"

# --- 3. نظام التنبيه الصوتي الأردني ---
class VoiceAlertSystem:
    def create_voice_alert(self, text):
        jordanian_text = f"يا قائد أبو سعود، {text}، الرعد معك دائماً."
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts = gTTS(text=jordanian_text, lang='ar', slow=False)
        tts.save(temp_file.name)
        return temp_file.name

    def send_voice_alert(self, message):
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            st.error("المفاتيح غير موجودة في 'الخزنة' يا قائد!")
            return
        
        voice_path = self.create_voice_alert(message)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
        try:
            with open(voice_path, 'rb') as v:
                requests.post(url, files={'voice': v}, data={'chat_id': TELEGRAM_CHAT_ID})
            os.unlink(voice_path)
        except Exception as e:
            st.error(f"فشل في إرسال التنبيه: {e}")

# --- 4. واجهة العمليات ---
st.title("🛡️ مركز الرعد الهجومي (Offensive Pro)")
tabs = st.tabs(["⚔️ اختبار الاختراق", "🔍 كشف التسلل", "📊 لوحة القيادة"])

hub = VoiceAlertSystem()
attacker = OffensiveModule()

with tabs[0]:
    st.header("وحدة الهجوم والاستطلاع")
    target = st.text_input("🎯 هدفك (IP/Domain):", placeholder="8.8.8.8")
    scan_type = st.selectbox("نوع العملية:", ["Port Scanning", "Packet Crafting", "Auth Bypass"])
    
    if st.button("🚀 تنفيذ بروتوكول الرعد"):
        if not target:
            st.warning("الهدف مفقود يا قائد.")
        else:
            with st.spinner("جاري المعالجة..."):
                if scan_type == "Port Scanning":
                    results = attacker.port_scanner(target, [21, 22, 80, 443, 3389])
                    st.code(f"نتائج الهدف {target}: {results}")
                    hub.send_voice_alert(f"فحصنا المنافذ للهدف، ولقينا {len(results)} منافذ مفتوحة.")
                
                elif scan_type == "Packet Crafting":
                    status, msg = attacker.packet_crafter(target)
                    if status == "SUCCESS":
                        st.success(msg)
                        hub.send_voice_alert("تم إرسال الحزمة بنجاح.")
                    else:
                        st.error(msg)
                        hub.send_voice_alert(f"انتبه، {msg}")

with tabs[2]:
    st.subheader("إحصائيات الترسانة")
    st.write(f"الحالة: {'متصل ✅' if TELEGRAM_TOKEN else 'غير متصل ❌'}")
    st.write(f"Scapy Ready: {'نعم' if SCAPY_AVAILABLE else 'لا (نظام محمي)'}")
