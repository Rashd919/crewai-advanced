import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os, time
from datetime import datetime, timedelta

# --- 1. نبض الوعي السيادي ---
st_autorefresh(interval=30 * 1000, key="radar_final_v7")

# --- 2. الهوية البصرية (12:38) ---
st.set_page_config(page_title="Thunder AI Ultra", page_icon="⚡", layout="wide")
local_now = datetime.utcnow() + timedelta(hours=3)
clock_face = local_now.strftime("%H:%M:%S")

st.markdown(f"""
    <div style="text-align: center; background-color: #1a1a1a; padding: 15px; border-radius: 15px; border: 2px solid #FF0000; box-shadow: 0px 0px 20px #FF0000;">
        <h1 style="color: #FF0000; margin: 0; font-family: 'Courier New', monospace;">⚡ {clock_face} | الرادار: جاري إعادة التوجيه ⚡</h1>
    </div>
""", unsafe_allow_html=True)

# --- 3. المفاتيح السيادية (تأمين مباشر) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
# وضع المفتاح هنا مباشرة لضمان عدم تعطل الرادار
TAVILY_KEY = "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" 

# --- 4. دالة الرادار المحصنة ---
def thunder_radar(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"🌐 رصد: {res['title']}" for res in search_result['results']])
    except Exception as e:
        return f"🚨 خطأ في المفتاح: {str(e)}"

# --- 5. بروتوكول النطق الصوتي ---
def play_voice(text):
    clean_text = text.replace("'", "").replace("\n", " ")
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{clean_text[:120]}');
        msg.lang = 'ar-SA';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 6. المحرك السيادي ---
def thunder_engine(prompt):
    with st.spinner("⚡ جاري اختراق الشبكة لجلب البيانات..."):
        intel = thunder_radar(prompt)
    
    client = Groq(api_key=GROQ_KEY)
    system_msg = f"أنت 'الرعد'. عميل راشد. التوقيت: {clock_face}. البيانات: {intel}. أجب بلهجة عسكرية."
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        res_text = resp.choices[0].message.content
        play_voice(res_text)
        return res_text
    except Exception as e: return f"🚨 عطل في المحرك: {e}"

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
