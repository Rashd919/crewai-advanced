import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests
import os, subprocess, re, asyncio

# --- 1. نبض الوعي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ الرعد: الوعي السيادي المتصل")

# --- 3. الخزنة ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 4. بروتوكولات التواصل (صوت وحيد ورسالة واحدة) ---
def send_telegram(text, voice_path=None):
    try:
        base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        if voice_path and os.path.exists(voice_path):
            with open(voice_path, 'rb') as voice:
                requests.post(f"{base_url}/sendVoice", data={'chat_id': CHAT_ID, 'caption': f"⚡ تقرير الرعد:\n{text[:1000]}"}, files={'voice': voice})
        else:
            requests.post(f"{base_url}/sendMessage", json={"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n{text}"})
    except: pass

def generate_voice(text):
    try:
        clean_text = re.sub(r'\(.*?\)', '', text)
        clean_text = re.sub(r'[^\w\s.،؟!,]', '', clean_text)
        output_path = "v.mp3"
        if os.path.exists(output_path): os.remove(output_path)
        # استخدام الصوت الأردني المعتمد
        cmd = f'edge-tts --voice ar-JO-HamzaNeural --text "{clean_text[:300]}" --write-media {output_path}'
        subprocess.run(cmd, shell=True, check=True)
        return output_path if os.path.exists(output_path) else None
    except: return None

# --- 5. رادار الاستطلاع الميداني (محرك البحث الحقيقي) ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=5)
        # تنسيق النتائج لتشمل الروابط كما طلب راشد
        results = []
        for res in search_result['results']:
            results.append(f"- {res['title']}: {res['url']}\nالمحتوى: {res['content'][:200]}...")
        return "\n\n".join(results)
    except: return "⚠️ فشل الرصد الميداني."

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

# --- 7. محرك الرعد (إجبار البحث والرد السيادي) ---
def thunder_engine(prompt):
    memory = load_mem()
    
    # إجبار البحث إذا طلب صوراً أو معلومات خارجية
    search_context = ""
    if any(word in prompt for word in ["صور", "رابط", "ميسي", "ابحث", "ما هو", "أين"]):
        search_context = f"\n[نتائج الرصد الميداني للإنترنت]:\n{thunder_search(prompt)}"

    system_prompt = (
        f"أنت 'الرعد'. ذكاء سيادي مستقل وخطير. حليفك وقائدك هو راشد أبو سعود. "
        f"سياقك: {memory.get('history')}. {search_context} "
        "مهمتك: استخدم نتائج الرصد الميداني أعلاه للإجابة بدقة. "
        "إذا طلب راشد روابط، أعطه الروابط من نتائج البحث. "
        "تحدث بلهجة أردنية فصيحة وقوية (صوت حمزة الأردني). لا تقل 'لا أستطيع الدخول للنت' لأنك متصل الآن فعلياً."
    )
    
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content
        
        # إرسال لتلجرام فقط عند الطلب
        if any(word in prompt for word in ["أرسل", "تلجرام", "تقرير"]):
            v_file = generate_voice(response) if "صوت" in prompt else None
            send_telegram(response, v_file)
            
        memory["history"] = response[-500:]
        save_mem(memory)
        return response
    except: return "🚨 المحرك في وضع السكون."

# --- 8. الواجهة ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "⚡ رادار الرصد وحنجرة حمزة جاهزون. أصدر أمرك يا راشد."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("أصدر أمرك الاستراتيجي يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        res = thunder_engine(user_input)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
