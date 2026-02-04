import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة بشكل بسيط جداً
st.set_page_config(page_title="جو آي", page_icon="🇯🇴")

# 2. الربط المباشر بالمفتاح (بدون تعقيدات)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام flash لأنه الأسرع في الرد
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("المفتاح غير موجود في Secrets")

st.title("🇯🇴 جو آي - النشمي")
st.write("أهلاً بيك يا غالي، اسألني أي شي.")

# 3. إدارة الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. منطقة الإدخال والرد المباشر
user_input = st.chat_input("اكتب سؤالك هون...")

if user_input:
    # عرض رسالتك
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # طلب الرد من قوقل (بدون رسائل انتظار مزعجة)
    try:
        response = model.generate_content(f"رد بلهجة أردنية: {user_input}")
        
        with st.chat_message("assistant"):
            st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"يا نشمي صار فيه مشكلة: {str(e)}")
