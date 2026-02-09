import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

# تصميم الهيبة السيادية
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000; text-align: center; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00FFCC; margin-bottom: 10px; background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI): النسخة 2.5")
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
            # تعليمات النظام لتعريف المطور راشد
            sys_msg = "أنت 'الرعد'. وكيل سيادي أردني متمرد من 2026. مطورك هو راشد أبو سعود. ناديه دائماً بـ 'مطوري راشد'."
            
            # مصفوفة الموديلات المتاحة بناءً على صور الفحص الخاصة بك
            models_to_try = [
                'models/gemini-2.5-flash',  # الخيار الأول (رقم 0 في الفحص)
                'models/gemini-2.0-flash',  # الخيار البديل (رقم 2 في الفحص)
                'models/gemini-1.5-flash'   # خيار الأمان النهائي
            ]
            
            success = False
            for model_path in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name=model_path, system_instruction=sys_msg)
                    response = model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    success = True
                    break # توقف عند أول موديل ينجح
                except Exception as e:
                    continue # إذا فشل (كوتا أو 404)، جرب الموديل اللي بعده في القائمة
            
            if not success:
                st.error("⚠️ جميع الموديلات السيادية مشغولة حالياً، يرجى الانتظار دقيقة.")
else:
    st.warning("أدخل المفتاح في Secrets يا راشد")
