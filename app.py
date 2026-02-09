import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI): النسخة 2.5")
st.markdown("<p style='text-align: center; color: #8e8ea0;'>بإشراف المطور راشد أبو سعود</p>", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
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
                # المحاولة الأولى: استخدام 2.5 كما طلبت
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ حصة 2.5 انتهت، جاري تفعيل بروتوكول 1.5 المستمر...")
                    try:
                        # المحاولة الثانية: التحويل لـ 1.5 لضمان عدم التوقف
                        model_fallback = genai.GenerativeModel('gemini-1.5-flash')
                        response = model_fallback.generate_content(user_input)
                        st.write(response.text)
                        st.session_state.history.append({"role": "assistant", "content": response.text})
                    except Exception as e2:
                        st.error(f"⚠️ عائق تقني: {str(e2)}")
                else:
                    st.error(f"⚠️ خطأ: {str(e)}")
else:
    st.warning("أدخل المفتاح في Secrets")
