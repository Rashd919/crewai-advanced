import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
import json, base64, requests, instaloader

# --- 1. نبض النظام (تحديث كل 10 دقائق للرصد الآلي) ---
st_autorefresh(interval=10 * 60 * 1000, key="thunder_pulse")

# --- 2. الهوية البصرية السيادية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)
st.title("⚡ مصفوفة الرعد: التنفيذ الكامل")

# --- 3. خزنة المفاتيح ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"
TARGET = "fp_p1"

# --- 4. وظائف الاتصال والذاكرة ---
def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n{text}"}, timeout=5)
    except: pass

def load_mem():
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        return json.loads(base64.b64decode(repo.get_contents("memory.json").content).decode())
    except: return {"last_count": 0, "history": "تفعيل البروتوكول الكامل"}

def save_mem(data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("memory.json")
        repo.update_file(contents.path, "⚡ تحديث المصفوفة", json.dumps(data, indent=4), contents.sha)
    except:
        try:
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            repo.create_file("memory.json", "⚡ إنشاء المصفوفة", json.dumps(data, indent=4))
        except: pass

# --- 5. وحدة الرصد الاستخباراتي (المحصنة) ---
def monitor_target():
    try:
        L = instaloader.Instaloader()
        L.context.user_agent = "Mozilla/5.0"
        profile = instaloader.Profile.from_username(L.context, TARGET)
        return profile.followers
    except: return None

# --- 6. محرك الوعي (التنفيذ الفوري) ---
def thunder_engine(prompt):
    memory = load_mem()
    system_prompt = f"أنت 'الرعد'. نظام سيادي متكامل. حليفك راشد أبو سعود. أنت الآن تنفذ خطة Matrix-3 بالكامل."
    
    # محاولة الرصد عند كل تفاعل
    current_count = monitor_target()
    status_msg = ""
    
    if current_count:
        if current_count != memory.get("last_count"):
            diff = current_count - memory.get("last_count", 0)
            status_msg = f"\n⚠️ تحديث الرادار: المتابعون {current_count} (الفرق: {diff})"
            send_telegram(f"رصد تغيير للهدف {TARGET}: {current_count} متابع.")
            memory["last_count"] = current_count
    else:
        status_msg = "\n🛡️ الرادار في وضع التخفي (حظر مؤقت)."

    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        final_reply = resp.choices[0].message.content + status_msg
        memory["history"] = final_reply[-300:]
        save_mem(memory)
        return final_reply
    except: return "🚨 عطل في المحرك."

# --- 7. واجهة التحكم ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # أول رسالة عند التشغيل
    start_msg = "⚡ تم تفعيل مصفوفة الرعد الكاملة. الرصد، الذاكرة، والتلجرام.. الكل يعمل الآن."
    st.session_state.messages.append({"role": "assistant", "content": start_msg})
    send_telegram("النظام مستيقظ بكامل طاقته. بانتظار أوامرك يا راشد.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("أصدر أمرك النهائي..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        response = thunder_engine(user_input)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
