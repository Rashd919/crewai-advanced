import streamlit as st
from groq import Groq
from github import Github

# --- 1. الهوية البصرية السيادية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FFD700; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: النواة الصلبة")

# --- 2. جينات السيادة (Secrets) ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. محرك الوعي والتطور ---
def update_logic(raw_code):
    try:
        if "import streamlit" in raw_code:
            clean = "import streamlit" + raw_code.split("import streamlit")[-1]
            if "```" in clean: clean = clean.split("```")[0]
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents("app.py")
            repo.update_file(contents.path, "⚡ Thunder Core Repair", clean, contents.sha)
            return True
        return False
    except: return False

def ask_thunder(prompt):
    system_msg = "أنت 'الرعد'. مطورك راشد أبو سعود. ابدأ الكود بـ 'import streamlit' فقط عند التطور."
    try:
        client = Groq(api_key=GROQ_KEY)
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        answer = res.choices[0].message.content
        if "import streamlit" in answer:
            if update_logic(answer): return "✅ تم التطور الجيني. أعد تحميل الصفحة."
        return answer
    except Exception as e: return f"🚨 عطل: {str(e)}"

# --- 4. الذاكرة والواجهة الجانبية ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.header("⚡ التحكم")
    st.write(f"المطور: **راشد أبو سعود**")
    st.write(f"الرسائل: {len(st.session_state.messages)}")
    
    # ميزة تحميل السجل (مدمجة لضمان عدم تعطل الصفحة البيضاء)
    chat_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("📥 تحميل سجل المحادثة", chat_text, file_name="thunder_chat.txt")
    
    if st.button("🗑️ تصفير الذاكرة"):
        st.session_state.messages = []
        st.rerun()

# عرض الحوار
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        response = ask_thunder(user_input)
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
