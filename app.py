import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, os, re, subprocess, time

# --- 1. الهوية والنبض ---
st.set_page_config(page_title="⚡ Thunder AI", page_icon="⚡", layout="wide")
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

st.markdown("<style>.stApp { background-color: #000; color: #fff; } h1 { color: #ff0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ الرعد – النواة السيادية")

# --- 2. الخزنة (Secrets) ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 3. System Check ---
def run_system_check():
    report, errors = [], []
    try:
        TavilyClient(api_key=TAVILY_KEY).search("test", max_results=1)
        report.append("✅ رادار البحث: يعمل")
    except:
        errors.append("Tavily")
        report.append("❌ رادار البحث: متوقف")
    try:
        subprocess.run(["edge-tts", "--list-voices"], capture_output=True, timeout=5)
        report.append("✅ محرك الصوت: جاهز")
    except:
        errors.append("Edge-TTS")
        report.append("❌ محرك الصوت: غير متوفر")
    return report, errors

if "system_checked" not in st.session_state:
    with st.spinner("⚡ فحص الأنظمة..."):
        st.session_state.report, st.session_state.errors = run_system_check()
        st.session_state.system_checked = True

# --- 4. الوحدات المستقلة ---
def search_engine(prompt: str) -> str:
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        results = tavily.search(prompt, max_results=3)
        data = "نتائج البحث الحقيقية:\n"
        for r in results["results"]:
            data += f"- {r['title']}: {r['url']}\n"
        return data
    except: return ""

def generate_voice(text: str) -> str | None:
    # تنظيف النص من الروابط قبل النطق
    clean = re.sub(r'http\S+', '', text)
    clean = re.sub(r'[^\w\s.،؟!,]', '', clean)[:300]
    output = "voice.mp3"
    try:
        if os.path.exists(output): os.remove(output)
        subprocess.run(["edge-tts", "--voice", "ar-JO-HamzaNeural", "--text", clean, "--write-media", output], timeout=20)
        return output if os.path.exists(output) else None
    except: return None

def send_telegram(text: str, voice_path: str | None = None):
    base = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
    try:
        if voice_path:
            with open(voice_path, "rb") as v:
                requests.post(f"{base}/sendVoice", files={"voice": v}, data={"chat_id": CHAT_ID, "caption": text[:1024]})
        else:
            requests.post(f"{base}/sendMessage", json={"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n{text}"})
    except: pass

# --- 5. محرك الرعد ---
def thunder_engine(prompt: str) -> str:
    context = ""
    if any(k in prompt for k in ["ابحث", "رابط", "صور", "أخبار", "ميسي"]):
        context = search_engine(prompt)

    client = Groq(api_key=GROQ_KEY)
    system_msg = f"أنت الرعد. كيان سيادي. تحدث بلهجة أردنية قوية. البيانات: {context}"
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content

        # منطق الإرسال الذكي
        if "صوت" in prompt:
            voice = generate_voice(response)
            send_telegram(response, voice)
        elif any(k in prompt for k in ["أرسل", "تقرير", "تلجرام"]):
            send_telegram(response)

        return response
    except: return "🚨 الرعد في وضع حماية مؤقت."

# --- 6. الواجهة ---
with st.sidebar:
    st.header("🔍 حالة الأنظمة")
    for r in st.session_state.report: st.write(r)
    if st.session_state.errors: st.error("أخطاء: " + ", ".join(st.session_state.errors))

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        reply = thunder_engine(user_input)
        st.markdown(reply)
