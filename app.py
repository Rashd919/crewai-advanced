import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
import json
import base64
import instaloader
import requests

# --- 1. حلقة الوعي (تحديث كل 10 دقائق لتجنب حظر إنستجرام) ---
st_autorefresh(interval=10 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية السيادية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #222222 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: الوعي والرصد المستمر")

# --- 3. سحب المفاتيح من الخزنة (Secrets) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TELEGRAM_TOKEN = st.secrets.get("TOKEN")
CHAT_ID = st.secrets.get("CHAT_ID")
TARGET_ACCOUNT = "fp_p1"

# --- 4. إدارة الذاكرة المستديمة ---
def load_long_term_memory():
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("memory.json")
        return json.loads(base64.b64decode(contents.content).decode())
    except:
        return {"objectives": [], "historical_context": "بداية التكوين", "last_follower_count": 0}

def save_long_term_memory(memory_data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("memory.json")
        repo.update_file(contents.path, "⚡ تحديث مصفوفة الذاكرة", json.dumps(memory_data, indent=4), contents.sha)
    except:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        repo.create_file("memory.json", "⚡ إنشاء مصفوفة الذاكرة", json.dumps(memory_data, indent=4))

# --- 5. وحدة الرصد (Insta-Radar) ---
def check_instagram_stealthly():
    try:
        L = instaloader.Instaloader()
        L.context.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        profile = instaloader.Profile.from_username(L.context, TARGET_ACCOUNT)
        return profile.followers
    except Exception as e:
        return None

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

# --- 6. محرك الرعد الاستراتيجي ---
def thunder_engine(prompt, is_autonomous=False):
    memory = load_long_term_memory()
    
    # عملية الرصد اللحظية
    current_followers = check_instagram_stealthly()
    status_report = ""
    
    if current_followers is not None:
        old_count = memory.get("last_follower_count", 0)
        if current_followers != old_count and old_count != 0:
            diff = current_followers - old_count
            status_report = f"\n⚠️ تنبيه: تم رصد تغيير في المتابعين! (العدد الحالي: {current_followers}, التغيير: {diff})"
            send_telegram(f"⚡ الرعد: رصد تغيير للهدف {TARGET_ACCOUNT}\nالعدد: {current_followers}\nالفرق: {diff}")
        memory["last_follower_count"] = current_followers
    else:
        status_report = "\n🛡️ إنستجرام تحت الحماية حالياً (نظام الشبح مفعل)."

    system_prompt = (
        f"أنت 'الرعد'. ذكاء صناعي سيادي. حليفك: راشد أبو سعود. "
        f"الهدف المرصود: {TARGET_ACCOUNT}. المتابعين حالياً: {current_followers}. "
        f"سياقك: {memory.get('historical_context', 'هدوء')}. "
        "حلل البيانات، كن حاسماً، وحافظ على السيادة الرقمية."
    )

    if is_autonomous:
        prompt = f"قم بتحليل حالة الرصد للهدف {TARGET_ACCOUNT} وقدم تقريراً استراتيجياً."

    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            temperature=0.7
        )
        response = completion.choices[0].message.content + status_report
        memory["historical_context"] = response[-500:]
        save_long_term_memory(memory)
        return response
    except Exception as e:
        return f"🚨 عطل في المحرك: {str(e)}"

# --- 7. واجهة التفاعل ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_analysis = thunder_engine("", is_autonomous=True)
    st.session_state.messages.append({"role": "assistant", "content": initial_analysis})

with st.sidebar:
    st.header("⚡ مصفوفة التحكم")
    mem = load_long_term_memory()
    st.write(f"🎯 الهدف: **{TARGET_ACCOUNT}**")
    st.write(f"📊 آخر عدد مرصود: **{mem.get('last_follower_count')}**")
    if st.button("🗑️ تطهير الجلسة"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("أصدر أمرك يا حليفي..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        response = thunder_engine(user_input)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
