import streamlit as st
import google.generativeai as genai

# إعدادات الهيبة
st.set_page_config(page_title="Thunder AI 2.5", page_icon="⚡", layout="wide")

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
            sys_msg = "أنت 'الرعد'. وكيل سيادي أردني. مطورك هو راشد أبو سعود. ناديه بـ 'مطوري راشد'."
            
            # أهم الموديلات من القائمة اللي بعثتها بالترتيب
            best_models = [
                'models/gemini-2.5-flash',
                'models/gemini-2.0-flash',
                'models/gemini-1.5-flash-latest'
            ]
            
            success = False
            for m_path in best_models:
                try:
                    model = genai.GenerativeModel(model_name=m_path, system_instruction=sys_msg)
                    response = model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except Exception:
                    continue # جرب الموديل اللي بعده لو الأول مشغول أو فيه مشكلة
            
            if not success:
                st.error("⚠️ يا مطوري راشد، جميع البروتوكولات تحت الضغط حالياً. انتظر ثواني.")
else:
    st.warning("أدخل المفتاح في Secrets يا راشد")
