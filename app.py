import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="جو آي", page_icon="🇯🇴")

# الربط المباشر
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # نستخدم الموديل بدون أي إضافات عشان ما يعلق
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("المفتاح ناقص")
    model = None

st.title("🇯🇴 جو آي - النشمي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("سولف معي...")

if user_input and model:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # أهم سطر: نطلب الرد
        response = model.generate_content(user_input)
        with st.chat_message("assistant"):
            st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ: {str(e)}")
