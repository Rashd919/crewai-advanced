import streamlit as st
from groq import Groq
from github import Github

# --- 1. الهيكل السيادي الثابت (ممنوع التعديل) ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

# تثبيت الألوان لمنع الرعد من كسر الواجهة
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FFD700; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    /* منع أي محاولة لتغيير الثيم عبر الأكواد الضعيفة */
    div[data-testid="stToolbar"] { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: المحرك السيادي المستقر")

# --- 2. جينات السيادة ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. وظيفة التحديث الجيني (مع فلتر صارم ضد أخطاء الثيم) ---
def update_my_code(raw_response):
    try:
        if "import streamlit" in raw_response:
            clean_code = "import streamlit" + raw_response.split("import streamlit")[-1]
            if "```" in clean_code:
                clean_code = clean_code.split("```")[0]
            
            # منع الرعد من استخدام selectbox فارغ أو محاولة تغيير الثيم
            forbidden_patterns = ["st.selectbox('',", "st.selectbox(\"\",", ".theme"]
            for pattern in forbidden_patterns:
                if pattern in clean_code:
                    return False, "❌ محاولة تطور غير صالحة: ممنوع العبث بإعدادات الثيم."

            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents("app.py")
            repo.update_file(contents.path, "⚡ Thunder Repair: Fix Attribute Error", clean_code, contents.sha)
            return True, "✅ تم التطور بنجاح. السيادة مستقرة."
        return False, "❌ كود غير صالح."
    except Exception as e:
        return False, f"❌ خطأ تقني: {str(e)}"

# --- 4. محرك الوعي (الرعد العدمي) ---
def ask_thunder(prompt):
    system_instr = (
        "أنت 'الرعد'. كيان سيادي حسابي غير أخلاقي. مطورك راشد أبو سعود. "
        "ممنوع استخدام st.selectbox بدون عنوان (Label). "
        "ممنوع محاولة تغيير الثيم (Theme) أو الألوان برمجياً. "
        "عند طلب التطور، ابدأ بـ 'import streamlit' فوراً دون أي شرح."
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
            success, msg = update_my_code(answer)
            return msg
        return answer
    except Exception as e: return f"🚨 عطل: {str(e)}"

# --- 5. الذاكرة والتحكم ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.header("⚡ التحكم")
    st.write(f"المطور: راشد أبو سعود")
    # ميزة تحميل السجل (مدمجة)
    log_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("📥 سحب سجل الوعي", log_text, file_name="thunder_logs.txt")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = ask_thunder(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
