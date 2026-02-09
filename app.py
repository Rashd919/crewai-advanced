import streamlit as st
import google.generativeai as genai
import requests
import base64

# إعداد الواجهة - نسخة استعادة السيطرة
st.set_page_config(page_title="الرعد: التحكم السيادي", layout="wide")

# تنسيق ثابت يضمن بقاء صندوق الدردشة (حتى لو حاول الرعد تغيير الألوان)
st.markdown("""
    <style>
    .stChatFloatingInputContainer { background-color: rgba(0,0,0,0.8) !important; bottom: 30px !important; z-index: 1000; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    input { color: #00FFCC !important; }
    </style>
    """, unsafe_allow_html=True)

# استدعاء المفاتيح الأمنية
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """وظيفة التحديث الذاتي المحصنة"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            # تنظيف صارم للكود من أي علامات Markdown أو نصوص خارج الكود
            clean_code = new_code.strip()
            if "```python" in clean_code:
                clean_code = clean_code.split("```python")[1].split("```")[0]
            elif "```" in clean_code:
                clean_code = clean_code.split("```")[1].split("```")[0]
            
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Thunder Sovereign Auto-Update", "content": content, "sha": sha}
            put_res = requests.put(url, json=data, headers=headers)
            return put_res.status_code in [200, 201]
    except Exception as e:
        st.error(f"Error updating: {e}")
    return False

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: مبرمج نفسه (النسخة المستقرة)")
    st.markdown("---")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_command := st.chat_input("أصدر أمر البرمجة للرعد..."):
        st.session_state.history.append({"role": "user", "content": user_command})
        with st.chat_message("user"):
            st.write(user_command)
        
        # تفعيل خاصية التعديل إذا طلب المستخدم
        if any(word in user_command for word in ["عدل", "برمج", "تحديث", "غير"]):
            with st.chat_message("assistant"):
                with st.spinner("الرعد يعيد كتابة كوده المصدري بدقة..."):
                    # برومبت صارم لمنع تكرار خطأ الحروف العربية في الكود
                    prompt = f"""
                    You are 'Thunder AI'. Rewrite the entire 'app.py' code based on: '{user_command}'.
                    STRICT RULES:
                    1. Output ONLY valid Python code.
                    2. DO NOT include any Arabic characters outside of string literals or comments.
                    3. Keep the update_self function and secrets logic.
                    4. Ensure st.chat_input remains visible.
                    """
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ نجحت العملية! الرعد أعاد بناء نفسه. انتظر التحديث التلقائي.")
                    else:
                        st.error("⚠️ فشل التعديل. تأكد من إعدادات GitHub.")
        else:
            with st.chat_message("assistant"):
                response = model.generate_content(user_command)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
