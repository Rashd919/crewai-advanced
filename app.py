import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime, timedelta

# --- 1. بروتوكول الهوية السيادية ---
local_now = datetime.utcnow() + timedelta(hours=3)
clock_face = local_now.strftime("%H:%M:%S")

st.set_page_config(page_title="Thunder Ultra Pro", page_icon="⚡", layout="wide")

# تهيئة العداد وجلسة العمل (إصلاح مشكلة الانهيار)
if "history" not in st.session_state: st.session_state.history = []
if "count" not in st.session_state: st.session_state.count = 0

# --- 2. الشريط الجانبي (Sidebar) - نسخة Gemini 100% ---
with st.sidebar:
    st.markdown("<h2 style='color: #FF0000;'>⚡ الرعد</h2>", unsafe_allow_html=True)
    st.write(f"مرحباً **أبو سعود**، من أين نبدأ؟")
    
    st.button("🎨 إنشاء صورة", use_container_width=True)
    st.button("📚 ساعدني في التعلّم", use_container_width=True)
    st.button("✨ عزز إنتاجيتي", use_container_width=True)
    
    st.divider()
    st.markdown("### المحادثات الأخيرة")
    with st.expander("💬 السجل الميداني", expanded=True):
        st.caption("شبكة Molthub الاستخباراتية")
        st.caption("تحليل مشروع الرعد")
        st.caption("أزمة جزيرة إبستين")
    
    st.divider()
    st.markdown("### 🕵️ ملاحظات سرية")
    st.text_area("سجل تحركات الأهداف...", height=100, key="secure_notes")
    st.button("حفظ في الذاكرة")

# --- 3. الواجهة المركزية وأيقونات التفاعل ---
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #FF0000; padding: 15px; border-radius: 15px; background-color: #1a1a1a;">
        <h2 style="color: #FF0000; margin: 0;">⚡ مركز القيادة | {clock_face}</h2>
    </div>
""", unsafe_allow_html=True)

def show_feedback_icons(index):
    cols = st.columns([1,1,1,1,1,1,10])
    icons = ["👍", "👎", "🔄", "📤", "📋", "⋮"]
    for i, icon in enumerate(icons):
        cols[i].button(icon, key=f"btn_{index}_{i}")

# --- 4. مركز الملحقات المطور (مطابق لصورتك الأخيرة) ---
def show_upload_tools():
    with st.expander("➕ إرفاق وسائط وملفات (الصور، الكاميرا، المستندات)", expanded=False):
        c1, c2, c3 = st.columns(3)
        img = c1.file_uploader("🖼️ رفع صورة للتحليل", type=['png', 'jpg', 'jpeg'])
        doc = c2.file_uploader("📎 رفع ملف استخباراتي", type=['pdf', 'txt'])
        if c3.button("📷 تشغيل الكاميرا"): st.info("جاري طلب إذن الوصول للكاميرا...")
        if img: st.image(img, caption="تم رصد الصورة بنجاح", width=200)

# --- 5. محرك الرعد الاستخباراتي ---
def thunder_engine(prompt):
    TAVILY_KEY = "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"
    try:
        # البحث الميداني لضمان دقة 100% (مثل سعر الذهب 101.200)
        tavily = TavilyClient(api_key=TAVILY_KEY)
        intel = tavily.search(query=prompt, search_depth="advanced")
        context = intel['results'][0]['content']
    except: context = "البيانات الميدانية غير متوفرة."

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        sys_msg = f"أنت الرعد، نسخة Gemini لراشد. التوقيت {clock_face}. السياق الميداني: {context}"
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content
    except: return "🚨 خطأ: تأكد من ضبط GROQ_API_KEY في Secrets."

# --- 6. ساحة الحوار ---
for i, m in enumerate(st.session_state.history):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant": show_feedback_icons(i)

show_upload_tools()

if inp := st.chat_input("أصدر أوامرك يا قائد..."):
    st.session_state.history.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        res = thunder_engine(inp)
        st.markdown(res)
        show_feedback_icons(len(st.session_state.history))
        st.session_state.history.append({"role": "assistant", "content": res})
