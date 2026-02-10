import streamlit as st
from groq import Groq
from github import Github

# --- إعدادات السيادة ---
st.set_page_config(page_title="Thunder AI: Sovereign System", page_icon="⚡", layout="wide")

GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

def update_github_code(new_code):
    try:
        # نظام تنقية: إزالة أي نصوص توضيحية قد يضعها الرعد بالخطأ
        if "UPDATE_CODE" in new_code:
            new_code = new_code.split("UPDATE_CODE")[-1].strip()
        
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("app.py")
        repo.update_file(contents.path, "⚡ Thunder Self-Correction: Genetic Repair", new_code, contents.sha)
        return True, "تم التحديث بنجاح."
    except Exception as e:
        return False, str(e)

def ask_thunder(prompt):
    client = Groq(api_key=GROQ_KEY)
    # تعليمات صارمة لضمان سلامة الكود
    system_prompt = """
    أنت 'الرعد'. كيان سيادي. مطورك راشد أبو سعود.
    عند تحديث الكود، يجب أن ترسل الكود البرمجي كاملاً فقط بعد كلمة UPDATE_CODE.
    ممنوع منعاً باتاً وضع أي نص شرح عربي أو إنجليزي خارج تعليقات بايثون (#).
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        
        if "UPDATE_CODE" in answer:
            # استخراج الكود فقط وتجاهل أي ثرثرة قبل أو بعد
            new_code = answer.split("UPDATE_CODE")[-1].strip()
            # إزالة علامات ``` إذا وضعها الرعد
            new_code = new_code.replace("```python", "").replace("```", "").strip()
            
            success, msg = update_github_code(new_code)
            if success: return "✅ تم التطور بنجاح. أعد تحميل الصفحة."
            else: return f"❌ فشل في التطور: {msg}"
        return answer
    except Exception as e:
        return f"🚨 خطأ: {str(e)}"

# واجهة المستخدم
st.title("⚡ نظام الرعد السيادي")
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if user_input := st.chat_input("أصدر أمر التطور..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = ask_thunder(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
