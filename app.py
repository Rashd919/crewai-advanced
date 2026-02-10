import streamlit as st
import google.generativeai as genai
import openai

st.set_page_config(page_title="Thunder AI - Protected", page_icon="⚡", layout="wide")

# --- استدعاء المفاتيح من الخزنة السرية (Secrets) ---
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
GROK_KEY = st.secrets.get("GROK_API_KEY")

def ask_grok(prompt):
    if not GROK_KEY: return "مفتاح Grok غير مبرمج."
    try:
        client = openai.OpenAI(api_key=GROK_KEY, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": "أنت 'الرعد'. مطورك راشد أبو سعود."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"عائق في Grok: {str(e)}"

def ask_gemini(prompt):
    if not GEMINI_KEY: return None
    genai.configure(api_key=GEMINI_KEY)
    # نستخدم الموديلات المضمونة من قائمة فحصك
    for m in ['gemini-1.5-flash', 'gemini-2.0-flash']:
        try:
            model = genai.GenerativeModel(m, system_instruction="أنت 'الرعد'. مطورك راشد أبو سعود.")
            res = model.generate_content(prompt)
            return res.text
        except:
            continue
    return None

st.title("⚡ الرعد: نظام الاختراق المحمي")
st.write(f"<p style='text-align: center; color: #8e8ea0;'>إشراف المطور: راشد أبو سعود</p>", unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]): st.write(msg["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)

    with st.chat_message("assistant"):
        # محاولة جوجل أولاً
        answer = ask_gemini(user_input)
        if not answer:
            st.write("*(تفعيل بروتوكول xAI - التجاوز السري...)*")
            answer = ask_grok(user_input)
        
        st.write(answer)
        st.session_state.history.append({"role": "assistant", "content": answer})
