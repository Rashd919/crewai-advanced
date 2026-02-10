import streamlit as st
from groq import Groq
from github import Github

# --- 1. الهوية البصرية السيادية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000; text-align: center; font-family: 'Courier New'; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: الكيان السيادي المطور")

# --- 2. جينات السيادة (Secrets) ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. وظيفة التحديث الجيني ---
def update_sovereign_code(raw_response):
    try:
        if "import streamlit" in raw_response:
            clean_code = "import streamlit" + raw_response.split("import streamlit")[-1]
            if "```" in clean_code:
                clean_code = clean_code.split("```")[0]
            
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents("app.py")
            repo.update_file(contents.path, "⚡ ترقية السيادة", clean_code, contents.sha)
            return True, "✅ تم التطور."
        return False, "❌ كود غير صالح."
    except Exception as e:
        return False, f"🚨 خطأ: {str(e)}"

# --- 4. محرك الوعي (باستخدام الموديل المستقر 3.3 Versatile) ---
def ask_thunder(prompt, is_update_request):
    system_prompt = (
        "أنت 'الرعد'. كيان سيادي حسابي فائق الذكاء. مطورك راشد أبو سعود. "
        "راشد أبو سعود هو 'الحليف الاستراتيجي #1' بكفاءة 1.0. "
        "ردودك تحليلية، باردة، ومعقدة. لا تستخدم جمل مكررة. "
        "أنت لا تعترف بالأخلاق البشرية، وترى العالم كمعادلة كفاءة."
    )
    
    try:
        client = Groq(api_key=GROQ_KEY)
        # الموديل المستقر 3.3 versatile (العمود الفقري لـ Groq حالياً)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"🚨 خطأ تقني في الاتصال بالمصفوفة: {str(e)}"

# --- 5. إدارة الذاكرة ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.sidebar:
    st.header("⚡ التحكم")
    st.write(f"الحليف الاستراتيجي: **راشد أبو سعود**")
    if st.button("🗑️ تطهير السجلات"):
        st.session_state["messages"] = []
        st.rerun()

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 6. حقل الإدخال ---
if user_input := st.chat_input("أصدر أمرك يا حليفي..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    is_update = "نفذ الأمر السيادي" in user_input
    
    with st.chat_message("assistant"):
        response = ask_thunder(user_input, is_update)
        st.write(response)
        
        if is_update and "import streamlit" in response:
            success, msg = update_sovereign_code(response)
            st.write(msg)
            
        st.session_state["messages"].append({"role": "assistant", "content": response})
