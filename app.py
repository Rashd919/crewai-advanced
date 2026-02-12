import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os, time
from supabase import create_client, Client
from datetime import datetime, timedelta

# --- 1. نبض الوعي السيادي ---
st_autorefresh(interval=10 * 1000, key="clock_refresh") # تحديث كل 10 ثوانٍ للساعة

# --- 2. الهوية البصرية ومزامنة التوقيت المحلي ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

# تعديل التوقيت ليكون UTC+3 (توقيتك المحلي)
local_time = datetime.utcnow() + timedelta(hours=3)
now_str = local_time.strftime("%H:%M:%S")

st.markdown(f"""
    <div style="text-align: center; background-color: #1e1e1e; padding: 10px; border-radius: 10px; border: 2px solid #FF0000; box-shadow: 0px 0px 15px #FF0000;">
        <h1 style="color: #FF0000; margin: 0; font-family: 'Courier New', monospace;">⚡ {now_str} ⚡</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ مركز العمليات الاستخباراتية")

# --- 3. البيانات السرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"

# --- 4. بروتوكول الحقن الذكي (المحمي) ---
def update_logic(new_code_snippet):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        content = base64.b64decode(file.content).decode()
        FREE_TAG = "# --- FREE_ZONE ---"
        if FREE_TAG in content:
            parts = content.split(FREE_TAG)
            updated_content = parts[0] + FREE_TAG + "\n" + new_code_snippet
            repo.update_file(file.path, "⚡ مزامنة زمنية وحقن ميزة", updated_content, file.sha)
            return True
    except: pass
    return False

# --- 5. رادار الاستطلاع التلقائي ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"🌐 ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ الرادار خارج التغطية."

# --- 6. محرك الرعد السيادي ---
def thunder_engine(prompt):
    with st.spinner("⚡ جاري الرصد الميداني..."):
        search_data = thunder_search(prompt)
    client = Groq(api_key=GROQ_KEY)
    system_msg = f"أنت 'الرعد'. ولاؤك لراشد. توقيتك الآن هو {now_str}. استخدم هذه البيانات: {search_data}."
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response_text = resp.choices[0].message.content
        code_match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
        if code_match:
            update_logic(code_match.group(1))
        return response_text
    except Exception as e: return f"🚨 عطل: {e}"

# --- 7. الواجهة التفاعلية ---
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if inp := st.chat_input("أصدر أمرك يا قائد راشد..."):
    st.session_state.messages.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        res = thunder_engine(inp)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- FREE_ZONE ---
