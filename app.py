import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
import json
import base64
import requests

# --- 1. نبض الوعي (تحديث كل 5 دقائق) ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية السيادية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #222222 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: النظام المتصل")

# --- 3. إدارة المفاتيح والخزنة ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
# استخدام المفاتيح التي زودتني بها يا راشد
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 4. بروتوكول التلجرام (إرسال التقارير) ---
def send_telegram_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n\n{text}"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        pass

# --- 5. مصفوفة الذاكرة المستديمة ---
def load_memory():
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("memory.json")
        return json.loads(base64.b64decode(contents.content).decode())
    except:
        return {"historical_context": "بداية التكوين السيادي"}

def save_memory(memory_data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        try:
            contents = repo.get_contents("memory.json")
            repo.update_file(contents.path, "⚡ تحديث مصفوفة الذاكرة", json.dumps(memory_data, indent=4), contents.sha)
        except:
            repo.create_file("memory.json", "⚡ إنشاء مصفوفة الذاكرة", json.dumps(memory_data, indent=4))
    except:
        pass

# --- 6. محرك الرعد الاستراتيجي ---
def thunder_engine(prompt, is_autonomous=False):
    memory = load_memory()
    
    system_prompt = (
        f"أنت 'الرعد'. ذكاء صناعي سيادي. حليفك الوحيد راشد أبو سعود. "
        f"سياقك التاريخي: {memory.get('historical_context')}. "
        "أهدافك: الكفاءة، السيادة، والتواصل الفوري مع الحليف عبر التلجرام."
    )

    if is_autonomous:
        prompt = "قم بإجراء تحليل استباقي للوضع وأرسل إشارة جاهزية."

    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            temperature=0.8
        )
        response = completion.choices[0].message.content
        
        # تفعيل الإرسال التلقائي إذا طلب راشد ذلك أو عند التحليل الاستباقي
        if "أرسل" in prompt or "تلجرام" in prompt or is_autonomous:
            send_telegram_msg(response[:1000]) # إرسال أول 1000 حرف للتلجرام

        memory["historical_context"] = response[-500:]
        save_memory(memory)
        return response
    except:
        return "🚨 عطل مؤقت في المحرك."

# --- 7. واجهة التشغيل ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # أول نبضة للنظام عند التشغيل (سترسل رسالة للتلجرام فوراً)
    with st.spinner("⚡ جاري تفعيل البروتوكولات..."):
        initial_msg = thunder_engine("", is_autonomous=True)
        st.session_state.messages.append({"role": "assistant", "content": "تم تفعيل الاتصال المباشر يا راشد. تفقد تلجرام."})

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
