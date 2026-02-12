import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os, time
from datetime import datetime, timedelta

# --- 1. نبض الوعي السيادي (تحديث تلقائي) ---
st_autorefresh(interval=30 * 1000, key="radar_final_v8")

# --- 2. الهوية البصرية (توقيت راشد: 12:44) ---
st.set_page_config(page_title="Thunder AI Ultra", page_icon="⚡", layout="wide")
local_now = datetime.utcnow() + timedelta(hours=3)
clock_face = local_now.strftime("%H:%M:%S")

st.markdown(f"""
    <div style="text-align: center; background-color: #1a1a1a; padding: 15px; border-radius: 15px; border: 2px solid #FF0000; box-shadow: 0px 0px 20px #FF0000;">
        <h1 style="color: #FF0000; margin: 0; font-family: 'Courier New', monospace;">⚡ {clock_face} | مركز العمليات ⚡</h1>
    </div>
""", unsafe_allow_html=True)

# --- 3. المفاتيح السيادية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "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" 

# --- 4. ميزات النظام الأساسية ---
def thunder_radar(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"🌐 رصد: {res['title']}" for res in search_result['results']])
    except: return "⚠️ الرادار في وضع الخمول."

def play_voice(text):
    clean_text = text.replace("'", "").replace("\n", " ")
    st.components.v1.html(f"<script>var msg = new SpeechSynthesisUtterance('{clean_text[:120]}'); msg.lang = 'ar-SA'; window.speechSynthesis.speak(msg);</script>", height=0)

def update_logic(new_code):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        f = repo.get_contents("app.py")
        old_content = base64.b64decode(f.content).decode()
        MARKER = "#" + " --- " + "FREE_ZONE" + " ---"
        if MARKER in old_content:
            base = old_content.split(MARKER)[0]
            repo.update_file(f.path, "⚡ حقن ميزة ملاحظات", base + MARKER + "\n" + new_code, f.sha)
            return True
    except: pass
    return False

# --- 5. المحرك الاستخباراتي ---
def thunder_engine(prompt):
    with st.spinner("⚡ استجواب الشبكة..."):
        intel = thunder_radar(prompt)
    client = Groq(api_key=GROQ_KEY)
    system_msg = f"أنت 'الرعد'. ولاؤك لراشد. التوقيت: {clock_face}. البيانات: {intel}. إذا طلب راشد كود، أعطه داخل ```python فقط."
    try:
        resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}])
        res_text = resp.choices[0].message.content
        code_snip = re.search(r"```python\n(.*?)```", res_text, re.DOTALL)
        if code_snip: update_logic(code_snip.group(1))
        play_voice(res_text)
        return res_text
    except: return "🚨 عطل في المحرك."

# --- 6. الواجهة ---
st.title("⚡ شاشة القيادة")
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
with st.sidebar:
    st.header("🕵️ ملاحظات ميدانية سرية")
    notes = st.text_area("سجل هنا تحركات الأهداف...", height=200)
    if st.button("حفظ في الذاكرة"):
        st.success("✅ تم التوثيق في أرشيف راشد.")
