import streamlit as st
import google.generativeai as genai
import requests
import base64

# إعدادات الواجهة مع ضمان ظهور صندوق الكتابة
st.set_page_config(page_title="الرعد: التحكم الذاتي", layout="wide")

# تثبيت تنسيق CSS يمنع اختفاء صندوق الكتابة
st.markdown("""
    <style>
    .stChatFloatingInputContainer {
        background-color: rgba(0,0,0,0.5) !important;
        bottom: 20px !important;
    }
    input {
        color: white !important;
        background-color: #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# استدعاء المفاتيح
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
    headers = {"Authorization": f"token {github_token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        sha = res.json().get('sha')
        clean_code = new_code.strip().replace("```python", "").replace("```", "")
        content = base64.b64encode(clean_code.encode()).decode()
        data = {"message": "تحديث سيادي من الرعد", "content": content, "sha": sha}
        requests.put(url, json=data, headers=headers)
        return True
    return False

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: مبرمج نفسه")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # صندوق الكتابة - تأكد من وجوده
    if user_command := st.chat_input("أصدر أمر البرمجة للرعد..."):
        st.session_state.history.append({"role": "user", "content": user_command})
        
        if any(word in user_command for word in ["عدل", "برمج", "تحديث", "غير"]):
            with st.spinner("الرعد يعيد كتابة منطقه..."):
                prompt = f"أنت الرعد. بناءً على هذا الطلب: '{user_command}'، اكتب كود Python كامل لملف app.py. تأكد أن صندوق chat_input يظل ظاهراً وواضحاً."
                response = model.generate_content(prompt)
                if update_self(response.text):
                    st.success("✅ تم التعديل! انتظر التحديث...")
                else:
                    st.error("❌ فشل التعديل.")
        else:
            response = model.generate_content(user_command)
            st.write(response.text)
            st.session_state.history.append({"role": "assistant", "content": response.text})
