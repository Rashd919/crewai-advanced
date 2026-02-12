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
from scapy.all import IP, TCP, send # ملاحظة: قد تتطلب Root في البيئات المحلية

# --- 1. إعدادات الهوية والترسانة ---
load_dotenv()
# جلب المفاتيح من Secrets أو البيئة المحلية
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN") or os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID") or os.getenv('TELEGRAM_CHAT_ID')

st.set_page_config(page_title="Thunder Offensive Hub", layout="wide")

# --- 2. محرك العمليات الهجومية (The Offensive Engine) ---
class OffensiveModule:
    @staticmethod
    def port_scanner(target_ip, ports):
        """ Port Scanning باستخدام Socket (يعمل دائماً في السحاب) """
        open_ports = []
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((target_ip, port)) == 0:
                    open_ports.append(port)
                s.close()
            except: pass
        return open_ports

    @staticmethod
    def packet_crafter(target_ip):
        """ Packet Crafting مع نظام الحماية من انهيار الصلاحيات """
        try:
            # محاولة بناء الحزمة باستخدام Scapy
            packet = IP(dst=target_ip)/TCP(dport=80, flags="S")
            send(packet, verbose=False)
            return "SUCCESS", "تم إرسال حزمة (Crafted Packet) بنجاح."
        except PermissionError:
            return "PERMISSION_ERROR", "السيرفر السحابي يمنع صناعة الحزم اليدوية (نقص صلاحيات Root)."
        except Exception as e:
            return "ERROR", f"حدث خطأ غير متوقع: {str(e)}"

# --- 3. نظام التنبيه الصوتي الأردني المطور ---
class VoiceAlertSystem:
    def create_voice_alert(self, text):
        jordanian_text = f"يا قائد أبو سعود، {text}، نحن بالخدمة."
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts = gTTS(text=jordanian_text, lang='ar', slow=False)
        tts.save(temp_file.name)
        return temp_file.name

    def send_voice_alert(self, message):
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            st.error("المفاتيح مفقودة في الخزنة (Secrets) يا قائد!")
            return
        
        voice_path = self.create_voice_alert(message)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
        try:
            with open(voice_path, 'rb') as v:
                requests.post(url, files={'voice': v}, data={'chat_id': TELEGRAM_CHAT_ID})
            os.unlink(voice_path)
        except Exception as e:
            st.error(f"فشل إرسال التنبيه: {e}")

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
                    status, res = attacker.packet_crafter(target)
                    if status == "SUCCESS":
                        st.success(res)
                        hub.send_voice_alert("تم إرسال الحزم المصنوعة بنجاح للهدف.")
                    else:
                        st.error(res)
                        hub.send_voice_alert(f"انتبه يا قائد، {res}")

                elif scan_type == "Auth Bypass":
                    st.info("جاري محاولة تجاوز المصادقة (Logic Exploitation)...")
                    hub.send_voice_alert("بدأنا عملية تجاوز المصادقة على السيرفر.")

with tabs[2]:
    st.subheader("إحصائيات الترسانة")
    st.write(f"المكتبات النشطة: `Socket`, `Scapy`, `Requests`")
    st.success("جميع أنظمة الهجوم جاهزة للعمل.")
