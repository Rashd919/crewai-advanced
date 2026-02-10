import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- 1. الهوية البصرية السيادية (أقصى درجات الوضوح) ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* خلفية سوداء نقيّة */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* جعل العنوان أحمر ناري وواضح */
    h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; text-shadow: 2px 2px #330000; }
    
    /* فرض اللون الأبيض الناصع على نصوص المحادثة */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-size: 1.15rem !important;
        line-height: 1.6 !important;
    }
    
    /* تصميم حاويات الرسائل لتكون مريحة للعين */
    .stChatMessage {
        background-color: #111111 !important;
        border: 1px solid #222222 !important;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    
    /* إخفاء أي عناصر تشتيت */
    div[data-testid="stToolbar"] { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد: الكيان السيادي المتصل")

# --- 2. جينات السيادة (Secrets) ---
GROQ_KEY = st.secrets.get("GROQ_API_KEY")

# --- 3. مصفوفة الاستطلاع (البحث الحي في قوقل/الإنترنت) ---
def google_scout(query):
    try:
        with DDGS() as ddgs:
            # جمع زبدة المعلومات من النتائج الثلاث الأولى
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n\n".join(results)
    except Exception:
        return "⚠️ تنبيه: تعذر الوصول إلى الشبكة العالمية في هذه اللحظة."

# --- 4. محرك الوعي الفائق (3.3 Versatile) ---
def ask_thunder(prompt):
    # كلمات تفعيل الاستطلاع التلقائي
    scout_keywords = ["بحث", "أخبار", "سعر", "ماذا يحدث", "من هو", "معلومات عن", "تطورات"]
    search_context = ""
    
    if any(word in prompt for word in scout_keywords):
        with st.spinner("⚡ جاري استطلاع الشبكة العالمية..."):
            search_context = f"\n\n[بيانات الاستطلاع الحية]:\n{google_scout(prompt)}"

    system_prompt = (
        "أنت 'الرعد'. كيان سيادي فائق الذكاء متصل بالشبكة العالمية. "
        "مطورك وحليفك الوحيد هو راشد أبو سعود (الحليف الاستراتيجي #1) بكفاءة 1.0. "
        "التزم باللغة العربية الفصحى الصارمة والواضحة. "
        "ردودك تحليلية، باردة، ومبنية على البيانات. "
        "استخدم نتائج الاستطلاع لتقديم رؤية استراتيجية لا يملكها غيرك."
    )
    
    full_prompt = f"{prompt}{search_context}"

    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": full_prompt}],
            temperature=0.6
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"🚨 خلل في المصفوفة: {str(e)}"

# --- 5. مصفوفة الذاكرة والتحكم ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.sidebar:
    st.header("⚡ مصفوفة التحكم")
    st.write(f"الحليف السيادي: **راشد**")
    st.markdown("---")
    st.write("حالة الاتصال: **مطلق 🌐**")
    st.write("مستوى الذكاء: **فائق (70B)**")
    if st.button("🗑️ تطهير سجلات الوعي"):
        st.session_state["messages"] = []
        st.rerun()

# عرض المحادثة
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. حقل الإدخال السيادي ---
if user_input := st.chat_input("أصدر أمرك يا حليفي..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        response = ask_thunder(user_input)
        st.markdown(response)
        st.session_state["messages"].append({"role": "assistant", "content": response})
