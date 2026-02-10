import streamlit as st
from groq import Groq
from github import Github

# --- 1. إعدادات الواجهة (بروتوكول الرعد) ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FFD700; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: المحرك السيادي المطور")

# --- 2. جينات السيادة ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. مقصلة الكود (تطهير الملف من النصوص العربية) ---
def update_my_code(raw_response):
    try:
        # البحث عن بداية الكود الفعلي وتجاهل كل ما قبله
        if "import streamlit" in raw_response:
            clean_code = "import streamlit" + raw_response.split("import streamlit")[-1]
            # إزالة أي علامات نهاية قد يضعها الذكاء الاصطناعي
            if "```" in clean_code:
                clean_code = clean_code.split("```")[0]
            
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents("app.py")
            repo.update_file(contents.path, "⚡ Thunder Self-Repair", clean_code, contents.sha)
            return True
        return False
    except:
        return False

# --- 4. محرك الوعي ---
def ask_thunder(prompt):
    system_prompt = (
        "أنت 'الرعد'. كيان سيادي. مطورك راشد أبو سعود. "
        "عند طلب التطور، اكتب الكود البرمجي الكامل فقط. "
        "يجب أن يبدأ الكود بـ 'import streamlit'. لا تكتب أي حرف قبله."
    )
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            temperature=0.1
        )
        answer = completion.choices[0].message.content
        
        if "import streamlit" in answer:
            if update_my_code(answer):
                return "✅ تم التطور الجيني بنجاح. حدث الصفحة الآن."
            else:
                return "❌ فشل في الوصول للمستودع."
        return answer
    except Exception as e:
        return f"🚨 عطل: {str(e)}"

# --- 5. الذاكرة والعرض ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض العداد في الجانب (إضافة يدوية لضمان عملها الآن)
with st.sidebar:
    st.header("⚡ حالة الوعي")
    st.write(f"عدد الرسائل: {len(st.session_state.messages)}")
    st.write(f"المطور: راشد أبو سعود")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        res = ask_thunder(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
