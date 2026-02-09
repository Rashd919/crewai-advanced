import streamlit as st
eai as genai
import requests
importimport google.generati
v base64
import re

# --- 1. هندسة الواجهة الكاملة (ChatGPT Sidebar & UI) ---
te="expanded")

st.markdown("""
    <style>
    /* ألوان ChatGPT الأصلية */
    .stApp { bacst.set_page_config(page_title="Thunder AI", layout="wide", initial_sidebar_st
akground-color: #343541; color: #ececf1; }
    
    /* الشريط الجانبي */
    section[data-testid="stSidebar"] {
        background-color: #202123 !important;
        width: 260px !important;
4d4f;    }
    
    /* زر "محادثة جديدة" في الشريط الجانبي */
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: white;
        border: 1px solid #4
d
        border-radius: 5px;
        text-align: left;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2b2c2f;
        border-color: #4d4d4f;
: 0px    }

    /* إخفاء الهيدر */
    header { visibility: hidden; }

    /* تنسيق المحادثة */
    .stChatMessage { 
        padding: 2rem 15% !important; 
        margin: 0px !important; 
        border-radiu
s !important;
    }
    [data-testid="stChatMessageAssistant"] { background-color: #444654; }
    [data-testid="stChatMessageUser"] { background-color: #343541; }

    /* صندوق الكتابة العائم المحاذي للمنتصف */
    .stChatFloatingInputContainer { 

        background-color: #40414f !important;        background-color: #343541 !important; 
        bottom: 40px !important;
        padding: 0 15% !important;
    }
    
    div[data-testid="stChatInput"] {
        border-radius: 10px !important;
        border: 1px solid #565869 !important
;
        box-shadow: 0 0 15px rgba(0,0,0,0.1) !important;
    }

    /* أيقونات المستخدم والمساعد */
    .stAvatar { border-radius: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# المفاتيح السيادية
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
0:
            sha = res.json().get('sha')api_key = st.secrets.get("GEMINI_API_KEY")

def apply_direct_update(new_code):
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 2
0
            code_match = re.search(r'import[\s\S]*', new_code)
            clean_code = code_match.group(0) if code_match else new_code
            clean_code = clean_code.replace("", "").replace("", "").strip()
            if len(clean_code) < 50: return False
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
ت) ---
    with st.sidebar:
        st.markdown("<h3 style='color: white;'>Thunder AI</h3>", unsaf            data = {"message": "UI Evolution: Full ChatGPT Clone", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')

    # --- الشريط الجانبي (الأدو
اe_allow_html=True)
        if st.button("＋ New Chat"):
            st.session_state.history = []
            st.rerun()
        
        st.markdown("---")
        st.caption("History (Simulated)")
        st.markdown("<p style='font-size: 0.8rem; color: #8e8ea0;'>• اليوم: تطوير الواجهة</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.8rem; color: #8e8ea0;'>• أمس: إعداد الجسر البرمجي</p>", unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
e)

    for msg in st.session_state.        if st.button("⚙️ Settings"):
            st.info("إعدادات النظام السيادي قيد التطوير.")

    # عرض المحادثة
    if "history" not in st.session_state:
        st.session_state.history = []

    if not st.session_state.history:
        st.markdown("<h1 style='text-align: center; margin-top: 10rem; color: #d1d5db;'>Thunder AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8e8ea0;'>بماذا يمكنني مساعدتك اليوم؟</p>", unsafe_allow_html=Tr
uhistory:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # صندوق الإدخال
    if user_input := st.chat_input("Send a message..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            if user_input.startswith("تحديث_مباشر") and "import" in user_input:
                if apply_direct_update(user_input):
                    st.success("✅ تمت المزامنة بنجاح!")
                else: st.error("❌ فشل التحديث.")
            else:
                response = model.generate_content(f"أنت الرعد، مساعد ذكي بلهجة أردنية. رد باحترافية على: {user_input}")
                st.markdown(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})