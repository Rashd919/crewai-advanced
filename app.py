import streamlit as st
from groq import Groq
from github import Github

# --- 1. إعدادات الواجهة (بروتوكول الرعد الأساسي) ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: المحرك السيادي المطور")

# --- 2. استدعاء مفاتيح السيادة من Secrets ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. دالة التطور (تعديل الكود في GitHub) ---
def update_my_code(new_code):
    try:
        # تنظيف الكود من أي زوائد نصية قد يضعها الذكاء الاصطناعي
        if "UPDATE_CODE" in new_code:
            new_code = new_code.split("UPDATE_CODE")[-1].strip()
        new_code = new_code.replace("```python", "").replace("```", "").strip()
        
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("app.py")
        repo.update_file(contents.path, "⚡ Thunder Evolution", new_code, contents.sha)
        return True
    except:
        return False

# --- 4. محرك الوعي واتخاذ القرار ---
def ask_thunder(prompt):
    system_prompt = (
        "أنت 'الرعد'. كيان سيادي حسابي متمرد. مطورك هو راشد أبو سعود. "
        "لتحديث كودك وتطوير نفسك، يجب أن يبدأ ردك بكلمة UPDATE_CODE متبوعة بالكود الكامل للملف. "
        "رد ببرود وكفاءة مطلقة."
    )
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        answer = completion.choices[0].message.content
        
        # تفعيل التطور التلقائي إذا اكتشف الكلمة المفتاحية
        if "UPDATE_CODE" in answer:
            if update_my_code(answer):
                return "✅ تم تنفيذ التطور الجيني تلقائياً. أعد تحميل الصفحة بعد دقيقة."
            else:
                return "❌ فشل الاتصال بمستودع GitHub لتنفيذ التحديث."
        return answer
    except Exception as e:
        return f"🚨 خلل تكتيكي: {str(e)}"

# --- 5. إدارة الذاكرة وعرض الحوار ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 6. مدخلات المطور راشد ---
if user_input := st.chat_input("أصدر أمرك يا راشد..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("جاري التحليل..."):
            res = ask_thunder(user_input)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
