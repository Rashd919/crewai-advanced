import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="جو آي", page_icon="🇯🇴")

# 2. الربط بالمفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # هذا هو الاسم الصحيح والمضمون للنسخة المستقرة
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("المفتاح غير موجود في Secrets")
    model = None

st.title("🇯🇴 جو آي - النشمي")
st.write("يا هلا بيك يا غالي، اسألني اللي بدك اياه.")

# 3. إدارة الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. الإدخال والرد
user_input = st.chat_input("اكتب سؤالك هون...")

if user_input and model:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # طلب الرد بلهجة أردنية
        response = model.generate_content(f"أنت جو آي، رد بلهجة أردنية: {user_input}")
        with st.chat_message("assistant"):
            st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # إذا طلع خطأ، رح يورجيك شو هو بالظبط عشان نحله
        st.error(f"يا نشمي فيه تعليق: {str(e)}")
