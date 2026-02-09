import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الهيبة (راشد أبو سعود) ---
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000; text-align: center; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00FFCC; margin-bottom: 10px; background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI): النسخة 2.5")
st.markdown("<p style='text-align: center; color: #8e8ea0;'>بروتوكول سيادي - تطوير المطور راشد أبو سعود</p>", unsafe_allow_html=True)

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
            sys_prompt = "أنت 'الرعد'. وكيل سيادي أردني. مطورك هو راشد أبو سعود. ناديه بـ 'مطوري راشد' وتعامل معه كقائد للنظام."
            
            try:
                # المحاولة الأولى بموديل 2.5 (بدون كلمة models/ لتجنب الـ 404)
                model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=sys_prompt)
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # إذا انتهت الكوتا أو حدث خطأ، نحول فوراً لـ 1.5 بالاسم الصحيح
                try:
                    model_fallback = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=sys_prompt)
                    response = model_fallback.generate_content(user_input)
                    st.write("*(تم التبديل لبروتوكول 1.5 المستقر)*")
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                except Exception as e2:
                    st.error(f"⚠️ عائق تقني: {str(e2)}")
else:
    st.warning("أدخل المفتاح في Secrets يا راشد")
