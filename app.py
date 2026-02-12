import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os
from gtts import gTTS
from supabase import create_client, Client

# --- 1. نبض الوعي والتشغيل الذاتي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية السيادية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)
st.title("⚡ مركز العمليات الاستخباراتية")

# --- 3. الخزنة الرقمية والسرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 4. بروتوكول الأرشفة السيادية ---
def vault_store_report(report_text):
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            sb = create_client(url, key)
            sb.from_('reports').insert([{"report": report_text}]).execute()
            return True
    except: pass
    return False

# --- 5. بروتوكول الحقن الذكي (يحمي الأساس ويضيف الجديد) ---
def update_logic(new_code_snippet):
    """يضمن إضافة الميزات في 'المنطقة الحرة' فقط دون لمس نواة النظام"""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        current_content = base64.b64decode(file.content).decode()
        tag = "# --- منطقة الإضافات الحرة ---"
        if tag in current_content:
            base_part = current_content.split(tag)[0]
            updated_content = base_part + tag + "\n" + new_code_snippet
        else:
            updated_content = current_content + "\n\n" + tag + "\n" + new_code_snippet
        repo.update_file(file.path, "⚡ إضافة ميزة سيادية جديدة", updated_content, file.sha)
        return True
    except: return False

# --- 6. بروتوكولات التواصل (تلغرام وصوت) ---
def send_telegram(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": f"⚡ تقرير استخباراتي:\n{text}"})
    except: pass

def generate_voice(text):
    try:
        tts = gTTS(text=text[:150], lang='ar')
        tts.save("report.ogg")
        return "report.ogg"
    except: return None

# --- 7. رادار الاستطلاع الميداني ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ فشل الرادار."

# --- 8. محرك الرعد السيادي (المطور) ---
def thunder_engine(prompt):
    search_context = ""
    if any(word in prompt for word in ["ابحث", "أخبار", "رصد"]):
        search_context = f"\nبيانات الرصد الميداني: {thunder_search(prompt)}"

    client = Groq(api_key=GROQ_KEY)
    system_msg = (
        f"أنت 'الرعد السيادي'. ولاؤك لراشد أبو سعود. {search_context} "
        "إذا طلب راشد تعديلاً برمجياً، أعطِ فقط الجزء الجديد من الكود داخل علامات ```python."
    )
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content

        # الأرشفة الصامتة وإرسال تلغرام
        vault_store_report(response)
        if len(response) > 50: send_telegram(response)

        # بروتوكول التنفيذ (حقن الكود الجديد فقط)
        code_match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
        if code_match:
            snippet = code_match.group(1)
            if update_logic(snippet):
                return response + "\n\n**✅ تم حقن الميزة الجديدة بنجاح! جاري التحديث...**"

        return response
    except Exception as e: return f"🚨 عطل: {str(e)}"

# --- 9. الواجهة التفاعلية ---
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if inp := st.chat_input("أصدر أمرك يا قائد راشد..."):
    st.session_state.messages.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        res = thunder_engine(inp)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- منطقة الإضافات الحرة ---
# الميزات التي يضيفها الرعد تظهر هنا دائماً دون المساس بما سبق.
