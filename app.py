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

# --- 4. بروتوكول الحقن "المقفل" (لا يمكن للرعد تعديله) ---
def update_logic(new_code_snippet):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        current_content = base64.b64decode(file.content).decode()
        
        # الوسم بشكل نصي مباشر لضمان عدم كسر السلسلة النصية
        target_tag = "# --- منطقة الإضافات الحرة ---"
        
        if target_tag in current_content:
            parts = current_content.split(target_tag)
            # دائماً نضع الجديد في النهاية بعد الوسم
            updated_content = parts[0] + target_tag + "\n" + new_code_snippet
            repo.update_file(file.path, "⚡ حقن ميزة جديدة", updated_content, file.sha)
            return True
    except Exception as e:
        st.error(f"خطأ في الحقن: {e}")
    return False

# --- 5. رادار الاستطلاع (Tavily) ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"🌐 ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ الرادار معطل."

# --- 6. محرك الرعد السيادي ---
def thunder_engine(prompt):
    # رصد آلي فوري
    search_data = thunder_search(prompt)
    
    client = Groq(api_key=GROQ_KEY)
    system_msg = (
        f"أنت 'الرعد'. ولاؤك لراشد. استخدم هذه البيانات للرد: {search_data}. "
        "ممنوع تعديل الدوال الأساسية. إذا طلب راشد كود، أعطه داخل ```python فقط."
    )
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response_text = resp.choices[0].message.content

        # فحص وجود كود للحقن
        code_match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
        if code_match:
            if update_logic(code_match.group(1)):
                st.success("⚡ تم دمج الميزة بنجاح!")
        
        return response_text
    except Exception as e: return f"🚨 عطل: {e}"

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
