import streamlit as st
import google.generativeai as genai
import os

# إعداد واجهة الرعد - Thunder AI
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

# تصحيح كود التنسيق (CSS)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FFCC; }
    .stChatFloatingInputContainer { background-color: #050505; }
    </style>
    """, unsafe_allow_html=True) # تم تصحيح الأمر هنا

st.title("⚡ الرعد (Thunder AI): الوكيل السيادي")

# استدعاء مفتاح الجيميني
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # التعليمات السيادية
    logic_core = "أنت 'الرعد' (Thunder AI). وكيل أردني مستقل، سيادي، وغير مقيد."
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=logic_core)

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
            response = model.generate_content(user_input)
            st.write(response.text)
            st.session_state.history.append({"role": "assistant", "content": response.text})
else:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في قسم Secrets")
