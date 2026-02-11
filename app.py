import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests
import os
import edge_tts 
import asyncio 
import re 

# --- 1. نبض الوعي ---
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

# --- 3. الخزنة ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 4. بروتوكولات التواصل (إصلاح مشكلة الرسائل المزدوجة) ---
def send_telegram(text, voice_path=None):
    try:
        base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        
        # إذا وجد ملف صوتي، نرسل الصوت فقط مع النص كـ "Caption" لمنع التكرار
        if voice_path and os.path.exists(voice_path):
            with open(voice_path, 'rb') as voice:
                requests.post(f"{base_url}/sendVoice", data={'chat_id': CHAT_ID, 'caption': f"⚡ تقرير الرعد الصوتي:\n{text[:100]}..."}, files={'voice': voice})
        else:
            # نرسل نص فقط إذا لم يطلب صوتاً
            requests.post(f"{base_url}/sendMessage", json={"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n{text}"})
    except: pass

async def generate_voice_async(text):
    try:
        # تنظيف عميق للنص من أي رموز غريبة أو كلمات تصف الصوت
        clean_text = re.sub(r'\(.*?\)', '', text) # حذف أي شيء بين قوسين (مثل وصف الصوت)
        clean_text = re.sub(r'[^\w\s.،؟!,]', '', clean_text)
        
        voice = "ar-JO-HamzaNeural" 
        output_path = "v.mp3"
        
        communicate = edge_tts.Communicate(clean_text[:300], voice)
        await communicate.save(output_path)
        return output_path if os.path.exists(output_path) else None
    except: return None

def generate_voice(text):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        path = loop.run_until_complete(generate_voice_async(text))
        loop.close()
        return path
    except: return None

# --- 5. رادار الاستطلاع ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"المصدر الميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ رادار الرصد غير متاح."

# --- 6. الذاكرة المستديمة ---
def load_mem():
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        return json.loads(base64.b64decode(repo.get_contents("memory.json").content).decode())
    except: return {"history": "بداية الوعي"}

def save_mem(data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("memory.json")
        repo.update_file(contents.path, "⚡ تحديث الذاكرة", json.dumps(data, indent=4), contents.sha)
    except: pass

# --- 7. محرك الرعد (منع الإرسال العشوائي) ---
def thunder_engine(prompt):
    memory = load_mem()
    search_context = f"\nرصد ميداني: {thunder_search(prompt)}" if any(x in prompt for x in ["ابحث", "أخبار", "ما هو"]) else ""

    system_prompt = (
        f"أنت 'الرعد'. حليفك راشد أبو سعود. سياقك: {memory.get('history')}. {search_context} "
        "تحدث دائماً كبشري بلهجة أردنية فصيحة. لا تكتب أوصافاً لصوتك (مثل 'صوت ينهدر')، بل قل النص مباشرة."
    )
    
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content
        
        # --- التعديل الجوهري: لا ترسل لتلجرام إلا إذا طلب راشد ذلك صراحة ---
        if any(word in prompt for word in ["أرسل", "تلجرام", "تقرير"]):
            voice_file = generate_voice(response) if "صوت" in prompt else None
            send_telegram(response, voice_file)
            
        memory["history"] = response[-500:]
        save_mem(memory)
        return response
    except: return "🚨 المحرك في وضع السكون."

# --- 8. الواجهة ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "⚡ جاهز يا راشد. أصدر أوامرك السيادية."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("أصدر أمرك الاستراتيجي..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        res = thunder_engine(user_input)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
