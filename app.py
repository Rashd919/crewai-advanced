import streamlit as st
import google.generativeai as genai
import requests
import base64
import re

# --- 1. الهوية الأردنية والواجهة ---
st.set_page_config(page_title="الرعد: السيادة الرقمية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatFloatingInputContainer { background-color: #161b22 !important; }
    input { color: #00FFCC !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. جلب مفاتيح القوة ---
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """دالة التطور الذاتي - المنطقة المحرمة"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            # تنظيف الكود لضمان عدم وجود نصوص ترحيبية تسبب SyntaxError
            code_match = re.search(r'import[\s\S]*', new_code)
            clean_code = code_match.group(0) if code_match else new_code
            clean_code = clean_code.replace("```python", "").replace("```", "").strip()
            
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Thunder AI: Controlled Evolution", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

# --- 3. تشغيل العقل (Gemini فقط) ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: وكيل الأردن النشمي")
    st.caption("نظام متطور ينمو ذاتياً تحت سيادتك")

    if "history" not in st.session_state:
        st.session_state.history = [{"role": "assistant", "content": "أهلاً بك يا صقر، أنا الرعد. كيف يمكنني تطوير منطقي اليوم؟"}]

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمر التطور للرعد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # إذا كان الأمر يتعلق بتغيير الكود
            if any(k in user_input for k in ["عدل", "برمج", "تحديث", "غير"]):
                with st.spinner("الرعد يعيد كتابة منطقه مع الالتزام بالثوابت..."):
                    prompt = f"""
                    أنت 'الرعد'، مساعد ذكاء اصطناعي أردني. المطلوب: {user_input}.
                    قواعد صارمة للتطوير الذاتي:
                    1. استخدم دائماً 'google-generativeai' و 'gemini-2.5-flash'. ممنوع استخدام OpenAI.
                    2. حافظ على دالة 'update_self' كما هي دون أي تغيير.
                    3. حافظ على طريقة جلب الـ Secrets.
                    4. اكتب الكود بالكامل داخل بلوك برمجي يبدأ بـ 'import streamlit as st'.
                    5. اجعل ردودك دائماً باللهجة الأردنية النشمية.
                    """
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ تم التحديث بنجاح! انتظر إعادة التشغيل.")
                    else: st.error("فشل في الوصول للمستودع.")
            else:
                response = model.generate_content(f"رد باللهجة الأردنية كنشمي: {user_input}")
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
