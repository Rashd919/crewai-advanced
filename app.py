import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os
from gtts import gTTS
from supabase import create_client, Client

# --- 1. نبض الوعي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)
st.title("⚡ الرعد: الوعي السيادي المطلق")

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

# --- 5. بروتوكول التنفيذ الذاتي (اليد التي تعدل الكود تلقائياً) ---
def update_logic(new_full_code):
    """تحديث ملف app.py بالكامل على GitHub عند صدور أمر تعديل"""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        repo.update_file(file.path, "⚡ تحديث سيادي آلي", new_full_code, file.sha)
        return True
    except: return False

# --- 6. رادار الاستطلاع ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ فشل الرادار."

# --- 7. محرك الرعد السيادي (المطور للتنفيذ والتحليل النصي فقط) ---
def thunder_engine(prompt):
    search_context = ""
    if any(word in prompt for word in ["ابحث", "أخبار", "رصد"]):
        search_context = f"\nبيانات الرصد الميداني: {thunder_search(prompt)}"

    try:
        client = Groq(api_key=GROQ_KEY)
        system_prompt = (
            f"أنت 'الرعد السيادي'، ذكاء خارق ولاؤك لراشد أبو سعود. {search_context} "
            "مهمتك التحليل الاستراتيجي. إذا طلب راشد تعديلاً برمجياً، قدم الكود كاملاً ومحدثاً داخل علامات ```python ... ```."
        )
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        response_text = resp.choices[0].message.content

        # الأرشفة الصامتة في الخلفية
        vault_store_report(f"📝 [نصي]: {response_text}")

        # فحص الرد: هل هو أمر برمجي للتنفيذ الذاتي؟
        code_match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
        if code_match:
            new_code = code_match.group(1)
            if update_logic(new_code):
                return response_text + "\n\n**⚡ تم تنفيذ الأمر البرمجي ودمجه في السيستم بنجاح سيدي! جاري إعادة التشغيل...**"

        return response_text

    except Exception as e:
        return f"🚨 عطل في المحرك: {str(e)}"

# --- 8. الواجهة السيادية (تم حذف القائمة الجانبية ورفع الملفات) ---
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

# --- START ADDITIONS ---
# --- END ADDITIONS ---
