import streamlit as st
import google.generativeai as genai
import requests
import base64
import re

# --- 1. تصميم واجهة ChatGPT الاحترافية المظلمة ---
st.set_page_config(page_title="الرعد v2.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #212121; color: #ececf1; }
    .stChatMessage { border-radius: 15px; padding: 18px; margin-bottom: 12px; }
    [data-testid="stChatMessageAssistant"] { background-color: #444654; border: 1px solid #565869; }
    [data-testid="stChatMessageUser"] { background-color: #212121; border: 1px solid #565869; }
    .stChatFloatingInputContainer { background-color: #343541 !important; border-top: 1px solid #565869; }
    input { color: #ffffff !important; background-color: #40414f !important; border-radius: 10px !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# جلب المفاتيح من الـ Secrets
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def apply_direct_update(new_code):
    """دالة استقبال النبضات البرمجية من Gemini"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            # استخراج الكود البرمجي الصافي فقط
            code_match = re.search(r'import[\s\S]*', new_code)
            clean_code = code_match.group(0) if code_match else new_code
            clean_code = clean_code.replace("```python", "").replace("```", "").strip()
            
            # منع التحديث إذا كان الكود فارغاً (لتجنب الشاشة السوداء)
            if len(clean_code) < 50: return False
            
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Final ChatGPT UI Fix", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

# --- 2. تشغيل العقل الذكي ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.markdown("<h2 style='text-align: center; color: #10a37f;'>⚡ Thunder AI v2.0</h2>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("تكلم مع الرعد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            # إذا أرسلت كوداً مع كلمة تحديث_مباشر
            if user_input.startswith("تحديث_مباشر") and "import" in user_input:
                with st.spinner("جاري مزامنة العقل الاستراتيجي..."):
                    if apply_direct_update(user_input):
                        st.success("✅ تم تحديث النظام! انتظر إعادة التشغيل.")
                    else: st.error("❌ الكود غير مكتمل أو هناك خطأ.")
            else:
                # رد طبيعي باللهجة الأردنية
                response = model.generate_content(f"أنت الرعد، مساعد ذكي بلهجة أردنية نشمية. رد على: {user_input}")
                st.markdown(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
