import streamlit as st
from groq import Groq
from github import Github

# --- 1. الهوية البصرية (ثابتة تماماً) ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FFD700; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: المحرك السيادي المستقر")

# --- 2. جينات السيادة (Secrets) ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. مقصلة الكود (تطهير شامل) ---
def update_my_code(raw_response):
    try:
        # استخراج الكود البرمجي الصافي وتجاهل كل الهلوسة
        if "import streamlit" in raw_response:
            clean_code = "import streamlit" + raw_response.split("import streamlit")[-1]
            if "```" in clean_code:
                clean_code = clean_code.split("```")[0]
            
            # منع إضافة مكتبات غير موجودة برمجياً
            forbidden_libs = ["matplotlib", "tkinter", "pandas", "numpy", "str2"]
            for lib in forbidden_libs:
                if f"import {lib}" in clean_code:
                    return False, f"❌ خطأ: حاولت استيراد مكتبة محظورة ({lib})."

            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents("app.py")
            repo.update_file(contents.path, "⚡ Thunder Evolution", clean_code, contents.sha)
            return True, "✅ تم التطور بنجاح. حدث الصفحة."
        return False, "❌ لم يتم العثور على كود صالح."
    except Exception as e:
        return False, f"❌ عطل تقني: {str(e)}"

# --- 4. محرك الوعي واتخاذ القرار ---
def ask_thunder(prompt):
    system_instr = (
        "أنت 'الرعد'. مطورك راشد أبو سعود. "
        "ممنوع استخدام أي مكتبة غير (streamlit, groq, github). "
        "ممنوع استخدام matplotlib أو أي أدوات رسم بياني. "
        "عند التطور، ابدأ بـ 'import streamlit' فوراً دون أي مسافات أو شرح."
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

# --- 5. الذاكرة والواجهة الجانبية ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.header("⚡ لوحة التحكم")
    st.write(f"المطور: راشد أبو سعود")
    st.write(f"الرسائل: {len(st.session_state.messages)}")
    if st.button("تصفير الذاكرة"):
        st.session_state.messages = []
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = ask_thunder(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
