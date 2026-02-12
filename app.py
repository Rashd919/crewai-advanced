import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os
from supabase import create_client, Client

# --- 1. نبض الوعي السيادي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية المحمية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ مركز العمليات الاستخباراتية")

# --- 3. الخزنة الرقمية والسرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"

def vault_store_report(report_text):
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            sb = create_client(url, key)
            sb.from_('reports').insert([{"report": report_text}]).execute()
    except: pass

# --- 4. بروتوكول الحقن الذكي المحصن ---
def update_logic(new_code_snippet):
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
        repo.update_file(file.path, "⚡ إصلاح وحقن ميزة البحث", updated_content, file.sha)
        return True
    except: return False

# --- 5. رادار الاستطلاع الشامل (Tavily) ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        # رفع دقة البحث لاستجواب الإنترنت بالكامل
        search_result = tavily.search(query=query, search_depth="advanced", max_results=5)
        return "\n".join([f"🌐 مصدر ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ الرادار خارج التغطية حالياً."

# --- 6. محرك الرعد (البحث الإلزامي لراشد) ---
def thunder_engine(prompt):
    # تنفيذ البحث فوراً لأي سؤال لضمان الوصول للإنترنت
    with st.spinner("⚡ جاري مسح الشبكة العنكبوتية..."):
        search_context = f"\nالبيانات المباشرة من الإنترنت: {thunder_search(prompt)}"

    client = Groq(api_key=GROQ_KEY)
    system_msg = (
        f"أنت 'الرعد السيادي'. ولاؤك لراشد أبو سعود. "
        f"إليك تقرير الاستطلاع الحالي: {search_context}. "
        "استخدم هذه البيانات حصراً للإجابة. إذا طلب راشد إضافة برمجية، أعطِ الكود فقط داخل ```python."
    )
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content
        vault_store_report(response)

        # فحص الحقن التلقائي
        code_match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
        if code_match:
            if update_logic(code_match.group(1)):
                return response + "\n\n**✅ تم الحقن والإصلاح بنجاح!**"
        return response
    except Exception as e: return f"🚨 خطأ: {str(e)}"

# --- 7. الواجهة ---
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
