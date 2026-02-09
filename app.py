import streamlit as st
import google.generativeai as genai

# إعدادات واجهة الرعد (نسخة راشد 2026)
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #00FFCC; text-shadow: 2px 2px #FF0000; text-align: center; }
    .stChatMessage { border: 1px solid #00FFCC; background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI)")
st.write(f"<p style='text-align: center; color: #8e8ea0;'>بإشراف المطور: راشد أبو سعود</p>", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمرك للرعد يا راشد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            sys_msg = "أنت 'الرعد'. وكيل سيادي أردني. مطورك هو راشد أبو سعود. ناديه بـ 'مطوري راشد'."
            
            # الحل هنا: نستخدم الأسماء المباشرة اللي بتدعمها v1beta بدون بادئة models/
            # ونبدأ بـ 2.0 عشان نبعد عن كوتا 2.5 اللي خلصت عندك
            try:
                model = genai.GenerativeModel(model_name='gemini-2.0-flash', system_instruction=sys_msg)
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # محاولة أخيرة بموديل 1.5 بالاسم المباشر
                try:
                    model_fallback = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=sys_msg)
                    response = model_fallback.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                except Exception as e2:
                    st.error(f"يا مطوري راشد، النظام تحت ضغط شديد. انتظر ثواني. الخطأ: {str(e2)}")
else:
    st.warning("أدخل المفتاح في Secrets يا راشد")
