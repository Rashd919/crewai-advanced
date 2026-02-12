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
from scapy.all import IP, TCP, send, sr1 # مكتبة صناعة الحزم

# --- 1. إعدادات الهوية والترسانة ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

st.set_page_config(page_title="Thunder Offensive Hub", layout="wide")

# --- 2. محرك العمليات الهجومية (The Offensive Engine) ---
class OffensiveModule:
    @staticmethod
    def port_scanner(target_ip, ports):
        """ Port Scanning باستخدام Socket """
        open_ports = []
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target_ip, port)) == 0:
                open_ports.append(port)
            s.close()
        return open_ports

    @staticmethod
    def packet_crafter(target_ip):
        """ Packet Crafting باستخدام Scapy (هجوم SYN) """
        # بناء حزمة مخصصة لتجاوز الفلترة
        packet = IP(dst=target_ip)/TCP(dport=80, flags="S")
        send(packet, verbose=False)
        return "تم إرسال حزمة (Crafted Packet) بنجاح."

    @staticmethod
    def auth_brute_force(url, user_list, pass_list):
        """ Auth Bypass محاكاة باستخدام Requests الهجومية """
        # منطق استغلال الثغرة لتجاوز المصادقة
        for user in user_list:
            for password in pass_list:
                # محاكاة طلب تسجيل دخول عدائي
                resp = requests.post(url, data={'user': user, 'pass': password})
                if resp.status_code == 200: return f"تم الاختراق! المستخدم: {user}"
        return "فشلت عملية التجاوز."

# --- 3. نظام التنبيه الصوتي الأردني المطور ---
class VoiceAlertSystem:
    def __init__(self):
        self.bot_name = "الرعد الاردني"
        
    def create_voice_alert(self, text):
        jordanian_text = f"يا قائد أبو سعود، {text}، نحن بالخدمة."
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts = gTTS(text=jordanian_text, lang='ar', slow=False)
        tts.save(temp_file.name)
        return temp_file.name

    def send_voice_alert(self, message):
        voice_path = self.create_voice_alert(message)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
        with open(voice_path, 'rb') as v:
            requests.post(url, files={'voice': v}, data={'chat_id': TELEGRAM_CHAT_ID})
        os.unlink(voice_path)

# --- 4. واجهة العمليات المركزية ---
st.title("🛡️ مركز الرعد الهجومي (Offensive Pro)")
tabs = st.tabs(["⚔️ اختبار الاختراق الذكي", "🔍 كشف التسلل", "📊 لوحة القيادة"])

hub = VoiceAlertSystem()
attacker = OffensiveModule()

with tabs[0]:
    st.header("وحدة الهجوم والاستطلاع (Network Targeting)")
    
    col1, col2 = st.columns(2)
    with col1:
        target = st.text_input("🎯 عنوان الهدف (IP/Domain):", placeholder="192.168.1.1")
        scan_type = st.selectbox("نوع العملية:", ["Port Scanning", "Packet Crafting", "Auth Bypass"])
    
    if st.button("🚀 تنفيذ العملية"):
        if not target:
            st.warning("حدد الهدف أولاً يا قائد.")
        else:
            with st.spinner("جاري تنفيذ بروتوكول الرعد..."):
                if scan_type == "Port Scanning":
                    results = attacker.port_scanner(target, [21, 22, 80, 443, 3389])
                    report = f"نتائج فحص المنافذ للهدف {target}: {results}"
                    st.code(report)
                    hub.send_voice_alert(f"خلصنا فحص المنافذ، لقينا {len(results)} منافذ مفتوحة.")
                
                elif scan_type == "Packet Crafting":
                    res = attacker.packet_crafter(target)
                    st.success(res)
                    hub.send_voice_alert("تم إرسال الحزم المصنوعة بنجاح للهدف.")

                elif scan_type == "Auth Bypass":
                    # محاكاة منطق استغلال الثغرة Exploit Logic
                    st.info("جاري محاولة تجاوز المصادقة (Logic Exploitation)...")
                    hub.send_voice_alert("بدأنا عملية تجاوز المصادقة على السيرفر.")

with tabs[2]:
    st.subheader("إحصائيات الترسانة")
    st.write(f"المكتبات النشطة: `Socket`, `Scapy`, `Requests (Attack Mode)`")
    st.success("جميع أنظمة الهجوم جاهزة للعمل.")
