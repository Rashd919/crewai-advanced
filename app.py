import streamlit as st
import google.generativeai as genai
import requests
import base64

# إعداد الواجهة السيادية
st.set_page_config(page_title="الرعد: السيادة الرقمية", layout="wide")

# ضمان بقاء صندوق الكتابة واضحاً مهما كانت الخلفية
st.markdown("""
    <style>
    .stChatFloatingInputContainer { background-color: rgba(10, 10, 10, 0.9) !important; bottom: 20px !important; border-top: 1px solid #00FFCC; }
    input { color: #00FFCC !important; background-color: #1A1A1A !important; }
    .main { background-color: #050505; }
    </style>
    """, unsafe_allow_html=True)

# المفاتيح من الـ Secrets
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """تحديث ملف app.py برمجياً على GitHub"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            # تنظيف الكود لضمان كود بايثون نقي فقط
            clean_code = new_code.strip()
            if "```python" in clean_code:
                clean_code = clean_code.split("```python")[1].split("```")[0]
            elif "```" in clean_code:
                clean_code = clean_code.split("```")[1].split("```")[0]
            
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Thunder AI: Self-Evolution Update", "content": content, "sha": sha}
            put_res = requests.put(url, json=data, headers=headers)
            return put_res.status_code in [200, 201]
    except:
        pass
    return False

if api_key:
    genai.configure(api_key=api_key)
    # استخدام الموديل الأحدث الذي يدعمه مفتاحك
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: وكيل الأردن السيادي")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمرك للرعد..."):
        # عرض رسالة المستخدم
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # إذا كان الأمر يتعلق بالبرمجة أو التحديث
            if any(k in user_input for k in ["برمج", "عدل", "تحديث", "غير"]):
                with st.spinner("الرعد يعيد هندسة منطقه الخاص..."):
                    prompt = f"Rewrite the current Streamlit app.py code to: {user_input}. Output ONLY the Python code block. Ensure it's clean and stable."
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ نجحت العملية! الرعد أعاد بناء نفسه. الصفحة ستحدث قريباً.")
                        st.session_state.history.append({"role": "assistant", "content": "تم تحديث منطقي بنجاح يا صقر. انتظر التحديث التلقائي."})
                    else:
                        st.error("⚠️ فشل التحديث. تأكد من إعدادات GitHub Token.")
            else:
                # رد حواري عادي
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
