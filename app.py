import streamlit as st
from groq import Groq
from github import Github

# --- 1. الإعدادات البصرية (ثابتة لا تتغير) ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FFD700; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: المحرك السيادي")

# --- 2. جينات السيادة ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. وظيفة التحديث الجيني (محمية) ---
def update_my_code(raw_response):
    try:
        start_marker = "import streamlit"
        if start_marker in raw_response:
            clean_code = start_marker + raw_response.split(start_marker)[-1]
            if "```" in clean_code:
                clean_code = clean_code.split("```")[0]
            
            # منع الرعد من إضافة فراغات عشوائية في البداية
            lines = [line for line in clean_code.split('\n') if line.strip() or line == '']
            final_code = '\n'.join(lines)

            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents("app.py")
            repo.update_file(contents.path, "⚡ Thunder Repair", final_code, contents.sha)
            return True
        return False
    except: return False

# --- 4. محرك الوعي ---
def ask_thunder(prompt):
    system_instr = (
        "أنت 'الرعد'. مطورك راشد أبو سعود. "
        "عند طلب التطور، اكتب الكود كاملاً. "
        "ممنوع وضع أي مسافات قبل 'import streamlit'. ابدأ من العمود صفر."
    )
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_instr}, {"role": "user", "content": prompt}],
            temperature=0.1
        )
        answer = completion.choices[0].message.content
        if "import streamlit" in answer:
            if update_my_code(answer): return "✅ تم التطور بنجاح. حدث الصفحة."
            else: return "❌ فشل التحديث."
        return answer
    except Exception as e: return f"🚨 عطل: {str(e)}"

# --- 5. الذاكرة والواجهة الجانبية ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.header("⚡ حالة الوعي")
    st.write(f"المطور: راشد أبو سعود")
    st.write(f"الرسائل: {len(st.session_state.messages)}")
    if st.button("تحليل الكود الحالي"):
        with st.expander("شرح النظام"):
            st.info("النظام محمي الآن ضد أخطاء الإزاحة والثرثرة العربية.")

# عرض الرسائل
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

# إدخال المطور
if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = ask_thunder(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
