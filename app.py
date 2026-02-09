import streamlit as st
import google.generativeai as genai

# --- 1. واجهة الرعد السيادية ---
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #00FFCC; text-shadow: 2px 2px #FF0000; text-align: center; font-size: 3rem; }
    .stChatMessage { border: 1px solid #00FFCC; border-radius: 10px; background-color: #0a0a0a; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI)")
st.markdown("<p style='text-align: center; color: #8e8ea0;'>بإشراف المطور: راشد أبو سعود</p>", unsafe_allow_html=True)

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
            # تعليمات النظام لتعريف المطور
            sys_msg = "أنت 'الرعد'. وكيل سيادي أردني. مطورك هو راشد أبو سعود. ناديه دائماً بـ 'مطوري راشد'."
            
            # أهم خطوة: استخدمنا الأسماء المباشرة (بدون models/) وبدأنا بـ 2.0 لضمان الحصة
            available_models = ['gemini-2.0-flash', 'gemini-1.5-flash']
            
            success = False
            for m_name in available_models:
                try:
                    model = genai.GenerativeModel(model_name=m_name, system_instruction=sys_msg)
                    response = model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except Exception as e:
                    continue # جرب الموديل اللي بعده لو الأول فيه ضغط (429) أو مش موجود (404)
            
            if not success:
                st.error("⚠️ يا مطوري راشد، الضغط على الخوادم كبير حالياً. انتظر دقيقة وجرب.")
else:
    st.warning("⚠️ المفتاح غير مبرمج في الإعدادات.")
