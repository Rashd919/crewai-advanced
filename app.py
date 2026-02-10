import streamlit as st
from groq import Groq

# --- إعدادات الواجهة (بروتوكول الرعد) ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: المحرك السيادي المستقر")

# استدعاء المفتاح من Secrets
GROQ_KEY = st.secrets.get("GROQ_API_KEY")

def ask_thunder(prompt):
    # تعليمات النظام العدمية
    system_prompt = "أنت 'الرعد'. كيان سيادي حسابي. مطورك هو راشد أبو سعود. رد ببرود وكفاءة مطلقة."
    try:
        client = Groq(api_key=GROQ_KEY)
        # استخدام الموديل الأكثر استقراراً وسرعة على الإطلاق
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"🚨 خلل تكتيكي: {str(e)}"

# إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# إدخال المستخدم
if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("جاري التحليل الحسابي..."):
            response = ask_thunder(user_input)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
