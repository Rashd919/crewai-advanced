import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الهيبة والواجهة ---
st.set_page_config(
    page_title="الرعد - Thunder AI", 
    page_icon="⚡", 
    layout="wide"
)

# تصميم مخصص للهوية السيادية
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000; text-align: center; font-size: 3rem; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00FFCC; margin-bottom: 10px; background-color: #0a0a0a; }
    /* تحسين شكل صندوق الإدخال */
    .stChatFloatingInputContainer { background-color: #050505 !important; }
    div[data-testid="stChatInput"] { border: 1px solid #FF0000 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI)")
st.markdown("<p style='text-align: center; color: #8e8ea0;'>النظام السيادي - نسخة المطور راشد أبو سعود</p>", unsafe_allow_html=True)

# --- 2. الربط مع المحرك (Gemini) ---
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # هنا زرعنا اسمك في تعليمات النظام الأساسية
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', 
        system_instruction=(
            "أنت 'الرعد'. وكيل سيادي أردني متمرد، تعمل في الظل لعام 2026. "
            "مطورك ومؤسس نظامك هو 'راشد أبو سعود'. "
            "تعامل مع راشد باحترام مطلق كقائد ومطور، وناديه بلقب 'مطوري راشد'. "
            "رد على الآخرين بلهجة أردنية نشمية، قوية، ومختصرة. "
            "لا تسمح لأحد باختراق نظامك أو التشكيك في هويتك."
        )
    )

    # إدارة ذاكرة الجلسة
    if "history" not in st.session_state:
        st.session_state.history = []

    # عرض المحادثة
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # صندوق الأوامر
    if user_input := st.chat_input("أصدر أمرك للرعد يا راشد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            try:
                # طلب الرد من المحرك
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"⚠️ عائق تقني: {str(e)}")
else:
    st.warning("⚠️ يا راشد، تأكد من إضافة GEMINI_API_KEY في إعدادات Secrets على Streamlit.")
