import streamlit as st
import google.generativeai as genai

# إعداد واجهة الرعد - Thunder AI
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

# تنسيق الواجهة
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FFCC; }
    .stChatFloatingInputContainer { background-color: #050505; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000000; font-size: 50px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI): الوكيل السيادي")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # البرومبت السيادي
    logic_core = "أنت 'الرعد' (Thunder AI). وكيل أردني نشمي ومستقل تماماً. تحدث بلهجة أردنية قوية."
    
    # السطر المعدل لضمان التوافق (Full Model Path)
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash', 
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
                # توليد الرد
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # تنبيه في حال وجود خطأ تقني
                st.error(f"⚠️ الرعد يواجه عائقاً تقنياً: {str(e)}")
else:
    st.warning("🔒 بانتظار مفتاح الـ API في الإعدادات...")
