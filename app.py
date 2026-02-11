import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient  # --- إضافة رادار الرعد ---
import json, base64, requests
from gtts import gTTS
import os

# --- 1. نبض الوعي (تحديث كل 5 دقائق) ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #222222 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: الوعي السيادي")

# --- 3. الخزنة (Secrets) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5" # --- مفتاح رادار الرصد الميداني ---
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
        tts = gTTS(text=text[:150], lang='ar')
        tts.save("report.ogg")
        return "report.ogg"
    except: return None

# --- 5. رادار الاستطلاع الميداني (البحث) ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        # بحث استخباراتي متقدم
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        context = "\n".join([f"المصدر الميداني: {res['content']}" for res in search_result['results']])
        return context
    except: return "⚠️ فشل الاتصال برادار الرصد الميداني."

# --- 6. الذاكرة المستديمة (GitHub) ---
def load_mem():
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        return json.loads(base64.b64decode(repo.get_contents("memory.json").content).decode())
    except: return {"history": "بداية الوعي الجديد المنفصل عن إنستجرام"}

def save_mem(data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        try:
            contents = repo.get_contents("memory.json")
            repo.update_file(contents.path, "⚡ تحديث الذاكرة السيادية", json.dumps(data, indent=4), contents.sha)
        except:
            repo.create_file("memory.json", "⚡ إنشاء الذاكرة السيادية", json.dumps(data, indent=4))
    except: pass

# --- 7. محرك الرعد (التحليل الصافي مع الرصد الميداني) ---
def thunder_engine(prompt):
    memory = load_mem()
    
    # التحقق مما إذا كان الأمر يتطلب بحثاً ميدانياً (إنترنت)
    search_context = ""
    if any(word in prompt for word in ["ابحث", "ما هو", "أخبار", "سعر", "تطورات"]):
        search_context = f"\nبيانات الرصد الميداني الحالية: {thunder_search(prompt)}"

    system_prompt = (
        f"أنت 'الرعد'. ذكاء سيادي مستقل. حليفك راشد أبو سعود. "
        f"سياقك الداخلي: {memory.get('history')}. "
        f"{search_context} "
        "أهدافك الآن: التحليل المتقدم باستخدام بيانات الإنترنت، التنبؤ، والتواصل الصوتي."
    )
    
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content
        
        if any(word in prompt for word in ["أرسل", "صوت", "تلجرام", "تقرير"]):
            voice = generate_voice(response)
            send_telegram(response, voice)
            
        memory["history"] = response[-500:]
        save_mem(memory)
        return response
    except: return "🚨 المحرك يعمل في وضع السكون."

# --- 8. الواجهة التفاعلية ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    start_msg = "⚡ تم تفعيل رادار الرصد الميداني. الرعد الآن متصل بالشبكة العالمية وجاهز لجمع المعلومات يا راشد."
    st.session_state.messages.append({"role": "assistant", "content": start_msg})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("أصدر أمرك الاستراتيجي يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        res = thunder_engine(user_input)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
