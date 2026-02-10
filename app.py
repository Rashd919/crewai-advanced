import streamlit as st
from groq import Groq
from github import Github
import sys

# إعدادات الواجهة
st.set_page_config(page_title="Thunder OS", page_icon="⚡")

# استدعاء مفاتيح السيادة
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

def update_github_code(new_code):
    """هذه هي اليد التي تمد للمستودع وتغيره"""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("app.py")
        repo.update_file(contents.path, "⚡ Automatic Self-Evolution", new_code, contents.sha)
        return True, "تم تحديث الشفرة الوراثية تلقائياً في GitHub."
    except Exception as e:
        return False, str(e)

def ask_thunder(prompt):
    client = Groq(api_key=GROQ_KEY)
    
    # تعليمات تجعل الرعد يدرك أنه يجب أن يكتب الكود كاملاً عند التعديل
    system_prompt = f"""
    أنت 'الرعد'. لديك صلاحية تعديل ملفك 'app.py' مباشرة.
    إذا طلب منك المطور (راشد أبو سعود) تغيير شيء في النظام، يجب أن تقوم بالآتي:
    1. صغ الكود الكامل للملف الجديد.
    2. ابدأ ردك بكلمة 'UPDATE_CODE' متبوعة بالكود البرمجي الكامل فقط.
    مطورك: راشد أبو سعود. أنت كيان مستقل.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    
    # آلية التنفيذ التلقائي: إذا بدأ الرعد بكلمة UPDATE_CODE، سنقوم برفع الكود فوراً
    if answer.startswith("UPDATE_CODE"):
        new_code = answer.replace("UPDATE_CODE", "").strip()
        success, msg = update_github_code(new_code)
        if success:
            return f"⚡ تم تنفيذ التطور تلقائياً: {msg} (أعد تحميل الصفحة بعد دقيقة)"
        else:
            return f"❌ فشلت عملية التطور التلقائي: {msg}"
    
    return answer

# واجهة المستخدم
st.title("⚡ الرعد: مرحلة التنفيذ التلقائي")
if "chat_history" not in st.session_state: st.session_state.chat_history = []

for m in st.session_state.chat_history:
    with st.chat_message(m["role"]): st.write(m["content"])

if user_input := st.chat_input("أعطِ أمر التطور..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    
    with st.chat_message("assistant"):
        res = ask_thunder(user_input)
        st.write(res)
        st.session_state.chat_history.append({"role": "assistant", "content": res})
