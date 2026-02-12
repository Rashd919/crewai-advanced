import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os
from supabase import create_client, Client

# --- 1. نبض الوعي السيادي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ مركز العمليات الاستخباراتية")

# --- 3. البيانات السرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"

# --- 4. بروتوكول الحقن الذكي المطور (نسخة الإصلاح) ---
def update_logic(new_code_snippet):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        current_content = base64.b64decode(file.content).decode()
        
        # استخدام البحث عن الوسم بشكل ثابت ومحمي
        tag = "# --- منطقة الإضافات الحرة ---"
        if tag in current_content:
            parts = current_content.split(tag)
            # الاحتفاظ بالجزء العلوي وحقن الجديد في النهاية
            updated_content = parts[0] + tag + "\n" + new_code_snippet
        else:
            updated_content = current_content + "\n\n" + tag + "\n" + new_code_snippet
            
        repo.update_file(file.path, "⚡ إصلاح وحقن ميزة برمجية", updated_content, file.sha)
        return True
    except: return False

# --- 5. رادار الاستطلاع (البحث التلقائي) ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=5)
        return "\n".join([f"🌐 مصدر ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ الرادار خارج التغطية."

# --- 6. محرك الرعد السيادي ---
def thunder_engine(prompt):
    # مسح الشبكة فوراً لضمان دقة البيانات
    with st.spinner("⚡ جاري مسح الشبكة العنكبوتية..."):
        search_context = f"\nتقرير الاستطلاع: {thunder_search(prompt)}"

    client = Groq(api_key=GROQ_KEY)
    system_msg = (
        f"أنت 'الرعد السيادي' لراشد أبو سعود. ولاؤك مطلق. "
        f"استخدم بيانات الإنترنت هذه للإجابة: {search_context}. "
        "عند طلب ميزة برمجية، أعطِ كود بايثون فقط داخل علامات ```python."
    )
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content

        # معالجة طلبات الحقن البرمجي
        code_match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
        if code_match:
            if update_logic(code_match.group(1)):
                return response + "\n\n**✅ تم الحقن بنجاح سيدي!**"
        return response
    except Exception as e: return f"🚨 عطل: {str(e)}"

# --- 7. الواجهة التفاعلية ---
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
