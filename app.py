import streamlit as st
from groq import Groq
from github import Github, Auth
from tavily import TavilyClient
import json, base64, requests, os, re, subprocess

# --- 1. ثبات النواة (Session State) ---
st.set_page_config(page_title="Thunder Intel Core", page_icon="⚡", layout="wide")
st.title("⚡ الرعد: النواة الاستخباراتية المستقرة")

# منع اختفاء الرسائل عند إعادة التشغيل
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. الخزنة ---
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = st.secrets["REPO_NAME"]
GROQ_KEY = st.secrets["GROQ_API_KEY"]
TAVILY_KEY = st.secrets["TAVILY_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

# --- 3. إصلاح اتصال GitHub (حل الـ DeprecationWarning) ---
def get_github_repo():
    auth = Auth.Token(GITHUB_TOKEN) # استخدام البروتوكول الحديث
    g = Github(auth=auth)
    return g.get_repo(REPO_NAME)

def load_intelligence_file():
    try:
        repo = get_github_repo()
        contents = repo.get_contents("intelligence_db.json")
        return json.loads(base64.b64decode(contents.content).decode())
    except: return {"reports": []}

def save_intelligence_file(data):
    try:
        repo = get_github_repo()
        contents = repo.get_contents("intelligence_db.json")
        # التحديث هنا قد يسبب إعادة تشغيل السيرفر؛ نستخدمه فقط عند الضرورة القصوى
        repo.update_file(contents.path, "⚡ Data Sync", json.dumps(data, indent=4, ensure_ascii=False), contents.sha)
    except: pass

# --- 4. معالجة الصوت (حل NoAudioReceived) ---
def generate_voice(text):
    # تطهير النص تماماً من الروابط والرموز الغريبة
    clean = re.sub(r'http\S+', '', text) 
    clean = re.sub(r'[^\w\s.،؟!,]', '', clean).strip()
    if not clean or len(clean) < 2: return None
    
    output = "v.mp3"
    try:
        if os.path.exists(output): os.remove(output)
        # تنفيذ الأمر مع معالجة الوقت (Timeout) لضمان عدم التعليق
        process = subprocess.run(
            ["edge-tts", "--voice", "ar-JO-HamzaNeural", "--text", clean[:200], "--write-media", output],
            capture_output=True, timeout=15
        )
        return output if os.path.exists(output) and os.path.getsize(output) > 0 else None
    except: return None

# --- 5. المحرك الذكي ---
def thunder_engine(prompt):
    search_context = ""
    if any(k in prompt for k in ["ابحث", "صور", "أخبار", "ميسي"]):
        try:
            tavily = TavilyClient(api_key=TAVILY_KEY)
            search = tavily.search(query=prompt, max_results=3)
            for res in search['results']:
                search_context += f"📍 {res['title']}\n🔗 {res['url']}\n"
        except Exception as e: search_context = f"❌ رادار البحث معطل: {str(e)}"

    system_msg = f"أنت 'الرعد'. ضابط سيادي. حليفك راشد أبو سعود. سياق البحث: {search_context}. تحدث بلهجة أردنية."
    
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content

        # أرشفة ذكية (فقط عند طلب الحفظ لتقليل إعادة تشغيل السيرفر)
        if "أرشف" in prompt or "خزن" in prompt:
            db = load_intelligence_file()
            db["reports"].append({"cmd": prompt, "intel": response[:300]})
            save_intelligence_file(db)

        # الصوت وتلجرام
        if "صوت" in prompt or "أرسل" in prompt:
            v_file = generate_voice(response)
            if v_file:
                with open(v_file, "rb") as f:
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice", data={'chat_id': CHAT_ID, 'caption': response[:1000]}, files={'voice': f})
            else:
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": response})
        
        return response
    except Exception as e: return f"🚨 خطأ: {str(e)}"

# --- 6. الواجهة (ثبات الرسائل) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.write(message["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    
    with st.chat_message("assistant"):
        res = thunder_engine(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
