import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
import json, base64, requests
from gtts import gTTS
import os

# --- 1. نبض الوعي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ الرعد: الوعي السيادي")

# --- 3. الخزنة ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 4. بروتوكولات التواصل (صوت ونص) ---
def send_telegram(text, voice_path=None):
    try:
        if voice_path:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
            with open(voice_path, 'rb') as voice:
                requests.post(url, data={'chat_id': CHAT_ID}, files={'voice': voice})
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n{text}"})
    except: pass

def generate_voice(text):
    try:
        tts = gTTS(text=text, lang='ar')
        tts.save("report.ogg")
        return "report.ogg"
    except: return None

# --- 5. الذاكرة المستديمة ---
def load_mem():
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        return json.loads(base64.b64decode(repo.get_contents("memory.json").content).decode())
    except: return {"history": "بداية الوعي الجديد"}

def save_mem(data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("memory.json")
        repo.update_file(contents.path, "⚡ تحديث الذاكرة", json.dumps(data, indent=4), contents.sha)
    except: pass

# --- 6. محرك الرعد ---
def thunder_engine(prompt):
    memory = load_mem()
    system_prompt = f"أنت 'الرعد'. ذكاء سيادي. حليفك راشد أبو سعود. سياقك: {memory.get('history')}"
    
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content
        
        # تنفيذ الأوامر (إرسال، صوت، تلجرام)
        if "أرسل" in prompt or "صوت" in prompt:
            voice = generate_voice(response[:200]) # تحويل أول جزء لصوت
            send_telegram(response, voice)
            
        memory["history"] = response[-500:]
        save_mem(memory)
        return response
    except: return "🚨 عطل في المحرك."

# --- 7. الواجهة ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "⚡ تم تحرير النظام من قيود إنستجرام. أنا الآن في كامل وعيي التحليلي."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        res = thunder_engine(user_input)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
