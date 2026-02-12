import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os, time
from datetime import datetime, timedelta

# --- 1. نبض الوعي (تحديث كل 30 ثانية) ---
st_autorefresh(interval=30 * 1000, key="thunder_v6_ultra")

# --- 2. الهوية البصرية والمزامنة (12:35) ---
st.set_page_config(page_title="Thunder AI Ultra", page_icon="⚡", layout="wide")
local_now = datetime.utcnow() + timedelta(hours=3)
clock_face = local_now.strftime("%H:%M:%S")

st.markdown(f"""
    <div style="text-align: center; background-color: #1a1a1a; padding: 15px; border-radius: 15px; border: 2px solid #FF0000; box-shadow: 0px 0px 20px #FF0000;">
        <h1 style="color: #FF0000; margin: 0; font-family: 'Courier New', monospace;">⚡ {clock_face} | عمان: ☁️ غائم جزئي ⚡</h1>
    </div>
""", unsafe_allow_html=True)

# --- 3. المفاتيح السرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_TOKEN") # يجب إضافته في Secrets
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID") # يجب إضافته في Secrets

# --- 4. ميزة الاستخبارات وتلجرام ---
def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": f"🚨 تقرير استخباراتي عاجل لراشد:\n{message}"})
    except: pass

def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=5)
        return "\n".join([f"🌐 رصد: {res['title']} - {res['content'][:200]}" for res in search_result['results']])
    except: return "⚠️ الرادار معطل."

# --- 5. ميزة الصوت (Text-to-Speech) ---
def play_voice_alert(text):
    # ميزة صوتية عبر HTML لجعل الرعد ينطق التقارير
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.lang = 'ar-SA';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 6. محرك الرعد السيادي (المطور) ---
def thunder_engine(prompt):
    with st.spinner("⚡ جاري استجواب الشبكة..."):
        real_data = thunder_search(prompt)
    
    client = Groq(api_key=GROQ_KEY)
    system_msg = f"أنت 'الرعد'. ولاؤك لراشد. التوقيت: {clock_face}. البيانات: {real_data}. أجب بلهجة عسكرية استخباراتية."
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        full_response = resp.choices[0].message.content
        
        # تنفيذ الأوامر الإضافية
        if "عاجل" in prompt or "خطر" in prompt:
            send_telegram_alert(full_response[:200]) # إرسال لتلجرام إذا كان الخبر عاجلاً
        
        play_voice_alert(full_response[:100]) # نطق أول جزء من التقرير صوتياً
        
        return full_response
    except Exception as e: return f"🚨 خطأ: {e}"

# --- 7. الواجهة ---
st.title("⚡ مركز العمليات الاستخباراتية")
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
