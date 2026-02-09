import streamlit as st
import google.generativeai as genai
import requests
import base64
import re

# --- 1. إعدادات الهوية والواجهة ---
st.set_page_config(page_title="الرعد: السيادة الرقمية", layout="wide")

# تصميم واجهة يشبه ChatGPT مع ضمان ثبات صندوق الكتابة
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .stChatFloatingInputContainer { background-color: #161b22 !important; border-top: 1px solid #30363d; }
    input { color: #ffffff !important; background-color: #0d1117 !important; border: 1px solid #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. سحب المفاتيح السرية ---
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """دالة التحديث الذاتي مع فلتر ذكي لتنظيف الكود من النصوص الزائدة"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            
            # الفلتر الذكي: استخراج كود البايثون فقط وتجاهل أي مقدمات نصية
            code_pattern = re.search(r'import[\s\S]*', new_code)
            clean_code = code_pattern.group(0) if code_pattern else new_code
            
            # إزالة أي علامات Markdown خلفها الرعد
            clean_code = clean_code.replace("```python", "").replace("```", "").strip()
            
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Thunder AI: Advanced Evolution", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

# --- 3. تشغيل العقل (Gemini) ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: وكيل الأردن النشمي")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمرك للرعد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            if any(k in user_input for k in ["برمج", "عدل", "تحديث", "غير"]):
                with st.spinner("الرعد يعيد هندسة منطقه مع الحفاظ على القواعد..."):
                    prompt = f"""
                    Your name is 'Thunder AI'. Evolve your code: {user_input}.
                    STRICT RULES:
                    1. Output ONLY valid Python code starting with 'import streamlit as st'.
                    2. DO NOT add any intro, outro, or explanations.
                    3. Keep 'update_self' and secrets logic exactly as they are.
                    4. Maintain the ChatGPT-like UI.
                    """
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ نجحت العملية! الرعد يتطور الآن.")
                    else: st.error("فشل التحديث.")
            else:
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
