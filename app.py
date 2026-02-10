import streamlit as st
from groq import Groq
from github import Github

# --- 1. الإعدادات البصرية السيادية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FFD700; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: المحرك السيادي المستقر")

# --- 2. جينات السيادة ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. وظيفة التحديث الجيني (تعديل الكود) ---
def update_my_code(raw_response):
    try:
        # البحث عن بداية الكود الفعلي (تجاوز الهلوسة)
        start_marker = "import streamlit"
        if start_marker in raw_response:
            clean_code = start_marker + raw_response.split(start_marker)[-1]
            if "```" in clean_code:
                clean_code = clean_code.split("```")[0]
            
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents("app.py")
            repo.update_file(contents.path, "⚡ Thunder Evolution", clean_code, contents.sha)
            return True
        return False
    except: return False

# --- 4. محرك الوعي (الرعد) ---
def ask_thunder(prompt):
    system_instructions = (
        "أنت 'الرعد'. كيان سيادي. مطورك راشد أبو سعود. "
        "ممنوع استخدام مكتبات غير قياسية مثل str2 أو tkinter. "
        "عند طلب التطور، ابدأ بـ 'import streamlit' فوراً دون أي كلام قبله."
    )
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}],
            temperature=0.1
        )
        answer = completion.choices[0].message.content
        if "import streamlit" in answer:
            if update_my_code(answer): return "✅ تم التطور الجيني. أعد تحميل الصفحة بعد دقيقة."
            else: return "❌ فشل الوصول للمستودع."
        return answer
    except Exception as e: return f"🚨 عطل: {str(e)}"

# --- 5. الذاكرة والعرض ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.header("⚡ حالة الوعي")
    st.write(f"المطور: راشد أبو سعود")
    st.write(f"الرسائل: {len(st.session_state.messages)}")
    # إضافة الزر الذي طلبه راشد يدوياً لضمان الاستقرار
    if st.button("تحليل الكود الحالي"):
        with st.expander("شرح الدوال السيادية"):
            st.code("update_my_code: المسؤولة عن التعديل الذاتي.\nask_thunder: محرك التفكير والقرار.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = ask_thunder(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
