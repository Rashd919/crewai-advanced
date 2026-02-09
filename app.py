import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-align: center; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI): النسخة 2.5")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # التعليمات السيادية
    logic_core = "أنت 'الرعد' (Thunder AI). وكيل أردني نشمي، سيادي، ومستقل تماماً."
    
    # استخدام الموديل اللي نجح في الفحص
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash', 
        system_instruction=logic_core
    )

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
            try:
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"⚠️ عائق تقني: {str(e)}")
else:
    st.warning("🔒 أدخل المفتاح في Secrets")
