import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة السيادية
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000; text-align: center; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00FFCC; margin-bottom: 10px; background-color: #0a0a0a; }
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
            try:
                # استخدمنا الموديل اللي كوتا تبعته بتتحمل ضغطك يا راشد
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction="أنت 'الرعد'. وكيل سيادي أردني متمرد. مطورك ومؤسسك هو راشد أبو سعود. ناديه بـ 'مطوري راشد' دائماً."
                )
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # لو صار أي ضغط، بنعطيه تنبيه بسيط
                st.error(f"⚠️ النظام تحت الضغط حالياً، انتظر ثواني يا مطوري راشد. الخطأ: {str(e)}")
else:
    st.warning("⚠️ تأكد من المفتاح في Secrets.")
