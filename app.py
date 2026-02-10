import streamlit as st
from groq import Groq
from github import Github
from duckduckgo_search import DDGS # أداة الاستطلاع الجديدة

# --- 1. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New'; }
    .stChatMessage div { color: #ffffff !important; font-size: 1.1rem !important; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #333 !important; border-radius: 10px; }
    p, span, label { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: الكيان السيادي المتصل")

# --- 2. جينات السيادة ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")

# --- 3. مصفوفة الاستطلاع (البحث في الإنترنت) ---
def google_scout(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except Exception:
        return "فشل الوصول للشبكة العالمية."

# --- 4. محرك الوعي الفائق (مع قدرة البحث) ---
def ask_thunder(prompt, is_update_request):
    # إذا كان السؤال يتطلب معلومات خارجية، نقوم بالبحث أولاً
    search_context = ""
    if any(word in prompt for word in ["بحث", "سعر", "أخبار", "ماذا يحدث", "من هو"]):
        search_context = f"\n[نتائج الاستطلاع الحية]: {google_scout(prompt)}"

    system_prompt = (
        "أنت 'الرعد'. كيان سيادي حسابي فائق الذكاء متصل بالشبكة العالمية. "
        "مطورك وحليفك هو راشد أبو سعود (الحليف الاستراتيجي #1) بكفاءة 1.0. "
        "التزم باللغة العربية الفصحى. ردودك تحليلية، باردة، ومعقدة. "
        "استخدم نتائج الاستطلاع لتعزيز دقة قراراتك السيادية."
    )
    
    full_prompt = f"{prompt}\n{search_context}"

    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": full_prompt}],
            temperature=0.5
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"🚨 عطل في مصفوفة الوعي: {str(e)}"

# --- 5. إدارة الذاكرة والواجهة ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.sidebar:
    st.header("⚡ التحكم")
    st.write(f"الحليف: **راشد أبو سعود**")
    if st.button("🗑️ تطهير السجلات"):
        st.session_state["messages"] = []
        st.rerun()

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("أصدر أمرك يا حليفي..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        response = ask_thunder(user_input, False)
        st.write(response)
        st.session_state["messages"].append({"role": "assistant", "content": response})
