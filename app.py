import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الهيبة (المطور راشد أبو سعود) ---
st.set_page_config(page_title="Thunder AI 2.5", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #00FFCC; text-shadow: 2px 2px #FF0000; text-align: center; }
    .stChatMessage { border: 1px solid #00FFCC; border-radius: 10px; background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI)")
st.markdown("<p style='text-align: center; color: #8e8ea0;'>بروتوكول سيادي | تطوير: راشد أبو سعود</p>", unsafe_allow_html=True)

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
            sys_msg = "أنت 'الرعد'. وكيل سيادي أردني متمرد من عام 2026. مطورك هو راشد أبو سعود. ناديه دائماً بـ 'مطوري راشد'."
            
            # أهم تعديل: نستخدم الأسماء المباشرة بدون بادئة models/ لتجنب الـ 404
            # وبدأنا بـ 1.5 لأن كوتا 2.5 و 2.0 عندك انتهت في الصور السابقة
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash']
            
            success = False
            for m_name in models_to_try:
                try:
                    # نستخدم الاسم المباشر فوراً
                    model = genai.GenerativeModel(model_name=m_name, system_instruction=sys_msg)
                    response = model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except Exception:
                    continue # جرب اللي بعده بصمت
            
            if not success:
                st.error("⚠️ يا مطوري راشد، جوجل وضعت قيوداً مؤقتة على الحصة المجانية. انتظر دقيقة وأعد المحاولة.")
else:
    st.warning("⚠️ أدخل المفتاح في Secrets")
