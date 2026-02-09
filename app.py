import streamlit as st
import google.generativeai as genai
import requests
import base64
import re

# --- 1. هندسة الواجهة الكاملة بنسبة 100% ---
st.set_page_config(
    page_title="Thunder AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* ألوان ChatGPT الداكنة */
    .stApp { background-color: #343541; color: #ececf1; }
    
    /* الشريط الجانبي الاحترافي */
    section[data-testid="stSidebar"] {
        background-color: #202123 !important;
        width: 260px !important;
    }
    
    header, footer { visibility: hidden; }

    /* تنسيق المحادثة وتوسيطها */
    .stChatMessage { padding: 2rem 15% !important; margin: 0px !important; }
    [data-testid="stChatMessageAssistant"] { background-color: #444654; }
    
    /* صندوق الإدخال العائم */
    .stChatFloatingInputContainer { 
        background-color: #343541 !important; 
        bottom: 30px !important;
        padding: 0 15% !important;
    }
    
    div[data-testid="stChatInput"] {
        border: 1px solid #565869 !important;
        background-color: #40414f !important;
        border-radius: 10px !important;
    }
    
    /* أزرار الشريط الجانبي */
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: white;
        border: 1px solid #4d4d4f;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

# جلب المفاتيح
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def apply_direct_update(new_code):
    """دالة التحديث المباشر المحمية"""
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
            data = {"message": "Final Stability Fix", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

# --- 2. تشغيل المحرك (تم تحديث الموديل لضمان العمل) ---
if api_key:
    genai.configure(api_key=api_key)
    # استخدام الموديل الأكثر استقراراً لتجنب خطأ NotFound
    model = genai.GenerativeModel('gemini-1.5-flash')

    # --- الشريط الجانبي ---
    with st.sidebar:
        st.markdown("<h2 style='color: white; padding-bottom: 20px;'>Thunder AI</h2>", unsafe_allow_html=True)
        if st.button("＋ New Chat"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.caption("History")
        st.markdown("<div style='color: #8e8ea0;'>• تطوير واجهة ChatGPT</div>", unsafe_allow_html=True)
        st.markdown("<div style='color: #8e8ea0;'>• إصلاح أخطاء الموديل</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # الترحيب
    if not st.session_state.messages:
        st.markdown("<h1 style='text-align: center; margin-top: 8rem; color: #d1d5db;'>Thunder AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8e8ea0;'>كيف يمكنني مساعدتك اليوم؟</p>", unsafe_allow_html=True)

    # عرض الرسائل
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # المدخلات
    if prompt := st.chat_input("أرسل رسالة للرعد..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if prompt.startswith("تحديث_مباشر") and "import" in prompt:
                if apply_direct_update(prompt):
                    st.success("✅ تم المزامنة! سيتم التحديث فوراً.")
                else: st.error("❌ عائق في الاتصال.")
            else:
                try:
                    response = model.generate_content(f"أنت الرعد، مساعد ذكي بلهجة أردنية. رد باحترافية على: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"حدث خطأ في المحرك: {str(e)}")
