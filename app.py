import streamlit as st
from groq import Groq
from github import Github, Auth
from tavily import TavilyClient
import json, base64, requests, os, re, subprocess

# --- 1. بروتوكول الفحص الذاتي (System Self-Check) ---
def run_system_check():
    report = []
    # فحص المفاتيح
    keys = {
        "GROQ_API_KEY": st.secrets.get("GROQ_API_KEY"),
        "TAVILY_KEY": st.secrets.get("TAVILY_KEY"),
        "GITHUB_TOKEN": st.secrets.get("GITHUB_TOKEN"),
        "TELEGRAM_TOKEN": st.secrets.get("TELEGRAM_TOKEN")
    }
    for name, key in keys.items():
        if key: report.append(f"✅ {name}: جاهز")
        else: report.append(f"❌ {name}: مفقود!")
    
    # فحص محرك الصوت
    try:
        result = subprocess.run(["edge-tts", "--list-voices"], capture_output=True)
        if result.returncode == 0: report.append("✅ محرك الصوت: جاهز")
    except: report.append("❌ محرك الصوت: غير مستقر")
    
    return report

# --- 2. الهوية وثبات الجلسة ---
st.set_page_config(page_title="Thunder Self-Evolving", page_icon="⚡", layout="wide")
st.title("⚡ الرعد: النواة ذاتية التحديث")

# تشغيل الفحص عند بدء التطبيق
if "check_done" not in st.session_state:
    st.session_state.check_report = run_system_check()
    st.session_state.check_done = True

with st.sidebar:
    st.header("🔍 تقرير الفحص الذاتي")
    for r in st.session_state.check_report:
        st.write(r)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. الخزنة وإدارة ملفات GitHub ---
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = st.secrets["REPO_NAME"]
GROQ_KEY = st.secrets["GROQ_API_KEY"]
TAVILY_KEY = st.secrets["TAVILY_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

def update_source_code(new_code):
    """دالة السيادة: تعديل الكود المصدري ورفعه لـ GitHub فوراً"""
    try:
        auth = Auth.Token(GITHUB_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("app.py")
        repo.update_file(contents.path, "⚡ الأمر السيادي: تحديث الكود الذاتي", new_code, contents.sha)
        return True
    except Exception as e:
        st.error(f"🚨 فشل التحديث السيادي: {str(e)}")
        return False

# --- 4. المحرك المركزي (مع منطق التعديل الذاتي) ---
def thunder_engine(prompt):
    # إذا كان الأمر هو "تعديل الكود"
    if "نفذ الأمر السيادي" in prompt or "عدل كودك" in prompt:
        # استرجاع الكود الحالي
        auth = Auth.Token(GITHUB_TOKEN)
        current_code = Github(auth=auth).get_repo(REPO_NAME).get_contents("app.py").decoded_content.decode()
        
        # طلب التعديل من LLM
        system_update_msg = f"أنت مبرمج خبير. هذا هو كودي الحالي:\n{current_code}\n\nالمطلوب من القائد راشد: {prompt}. أعد كتابة الكود كاملاً مع التعديلات المطلوبة فقط بدون أي شرح."
        
        try:
            client = Groq(api_key=GROQ_KEY)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_update_msg}, {"role": "user", "content": "أعطني الكود المحدث الآن"}]
            )
            new_code = resp.choices[0].message.content
            # تنظيف الكود من علامات الماركداون إذا وجدت
            new_code = re.sub(r'```python|```', '', new_code).strip()
            
            if update_source_code(new_code):
                return "✅ تم تنفيذ الأمر السيادي يا راشد. جاري إعادة تشغيل النواة بالكود الجديد خلال ثوانٍ..."
            else:
                return "❌ فشل تحديث النواة."
        except Exception as e:
            return f"🚨 خطأ في معالجة التعديل: {str(e)}"

    # المنطق العادي للرعد (بحث وصوت)
    system_msg = "أنت 'الرعد'. ضابط أردني سيادي. حليفك راشد أبو سعود. تحدث بلهجة أردنية عسكرية."
    client = Groq(api_key=GROQ_KEY)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

# --- 5. الواجهة ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.write(message["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = thunder_engine(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
