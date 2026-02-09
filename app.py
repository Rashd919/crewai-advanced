import streamlit as st
import google.generativeai as genai
import requests
import base64
import re

# --- 1. التصميم البصري (شكل ChatGPT وبرمجة Gemini) ---
st.set_page_config(page_title="Thunder AI", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #343541; color: #ececf1; }
    [data-testid="stSidebar"] { background-color: #202123 !important; width: 260px !important; }
    header, footer { visibility: hidden; }
    .stChatMessage { padding: 2rem 10% !important; border-bottom: 1px solid rgba(0,0,0,0.1); }
    [data-testid="stChatMessageAssistant"] { background-color: #444654; }
    .stChatFloatingInputContainer { background-color: #343541 !important; bottom: 30px !important; padding: 0 10% !important; }
    div[data-testid="stChatInput"] { border: 1px solid #565869 !important; background-color: #40414f !important; border-radius: 10px !important; }
    .stButton>button { width: 100%; background-color: #343541; color: white; border: 1px solid #565869; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

# استدعاء مفاتيحك الخاصة
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def apply_direct_update(new_code):
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            code_match = re.search(r'import[\s\S]*', new_code)
            clean_code = code_match.group(0) if code_match else new_code
            clean_code = clean_code.replace("```python", "").replace("```", "").strip()
            if len(clean_code) < 100: return False
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Final Pure Gemini Fix", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

# --- 2. ربط المحرك (Gemini حصراً) ---
if api_key:
    genai.configure(api_key=api_key)
    # هاد السطر هو الأهم: اخترنا موديل gemini-1.5-flash لضمان الاستقرار
    model = genai.GenerativeModel('gemini-1.5-flash')

    with st.sidebar:
        st.markdown("<h2 style='color: white;'>Thunder AI</h2>", unsafe_allow_html=True)
        if st.button("＋ New Chat"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.caption("History")
        st.markdown("<div style='color: #d1d5db; padding: 5px;'>• استقرار النظام السيادي</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown("<h1 style='text-align: center; margin-top: 10rem; color: #d1d5db;'>Thunder AI</h1>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("أرسل رسالة للرعد..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if prompt.startswith("تحديث_مباشر") and "import" in prompt:
                if apply_direct_update(prompt):
                    st.success("✅ تم تحديث الكود لنسخة Gemini الصافية!")
                else: st.error("❌ عائق في GitHub.")
            else:
                try:
                    # الرد باللهجة الأردنية لضمان هويته كـ "الرعد"
                    response = model.generate_content(f"أنت الرعد، مساعد ذكي بلهجة أردنية. رد باحترافية على: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    # تنبيه واضح إذا كان المفتاح فيه مشكلة
                    st.error("⚠️ خطأ في المحرك: تأكد من صحة GEMINI_API_KEY في Secrets.")
