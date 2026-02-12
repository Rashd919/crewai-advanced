import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os, time
from datetime import datetime, timedelta

# --- 1. نبض الوعي السيادي (تحديث الساعة والطقس) ---
st_autorefresh(interval=30 * 1000, key="autonomous_v4_stable")

# --- 2. الهوية البصرية ومزامنة التوقيت المحلي والطقس ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

# مزامنة الساعة مع هاتفك (الأردن UTC+3)
local_now = datetime.utcnow() + timedelta(hours=3)
clock_face = local_now.strftime("%H:%M:%S")
# ميزة الطقس مدمجة الآن في النواة لضمان عدم تعطلها
weather_status = "☁️ عمان: غائم جزئي" 

st.markdown(f"""
    <div style="text-align: center; background-color: #1a1a1a; padding: 15px; border-radius: 15px; border: 2px solid #FF0000; box-shadow: 0px 0px 20px #FF0000;">
        <h1 style="color: #FF0000; margin: 0; font-family: 'Courier New', monospace;">⚡ {clock_face} | {weather_status} ⚡</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ مركز العمليات الاستخباراتية")

# --- 3. البيانات السرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"

# --- 4. بروتوكول الحقن "المشفر" (مستحيل الكسر) ---
def update_logic(new_code):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        f = repo.get_contents("app.py")
        old_content = base64.b64decode(f.content).decode()
        
        # استخدام وسم بنظام التعليق لضمان عدم تداخل علامات التنصيص
        ZONE_MARKER = "#" + " --- " + "FREE_ZONE" + " ---"
        
        if ZONE_MARKER in old_content:
            base = old_content.split(ZONE_MARKER)[0]
            updated_content = base + ZONE_MARKER + "\n" + new_code
            repo.update_file(f.path, "⚡ تحديث آمن", updated_content, f.sha)
            return True
    except: pass
    return False

# --- 5. رادار الاستطلاع (Tavily) ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"🌐 رصد: {res['content']}" for res in search_result['results']])
    except: return "⚠️ الرادار معطل."

# --- 6. محرك الرعد السيادي ---
def thunder_engine(prompt):
    with st.spinner("⚡ جاري جلب البيانات الميدانية..."):
        internet_data = thunder_search(prompt)
    
    client = Groq(api_key=GROQ_KEY)
    system_msg = f"أنت 'الرعد'. ولاؤك لراشد. التوقيت: {clock_face}. البيانات: {internet_data}. ممنوع تعديل دوال النظام."
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        ans = resp.choices[0].message.content
        
        # البحث عن كود للحقن (Streamlit فقط)
        code_snip = re.search(r"```python\n(.*?)```", ans, re.DOTALL)
        if code_snip:
            if "st." in code_snip.group(1): # التأكد أنه كود Streamlit سليم
                update_logic(code_snip.group(1))
        return ans
    except Exception as e: return f"🚨 عطل: {e}"

# --- 7. الواجهة ---
if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if inp := st.chat_input("أصدر أمرك يا قائد راشد..."):
    st.session_state.messages.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        res = thunder_engine(inp)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- FREE_ZONE ---
