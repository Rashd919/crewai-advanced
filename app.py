import streamlit as st
from groq import Groq
from tavily import TavilyClient
import base64, requests, re
from datetime import datetime, timedelta

# --- 1. إعدادات الهوية والبيانات السرية ---
local_now = datetime.utcnow() + timedelta(hours=3)
clock_face = local_now.strftime("%H:%M")

st.set_page_config(page_title="Thunder Gemini Ultimate", page_icon="⚡", layout="wide")

# استرجاع المفاتيح من Secrets
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "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"
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID")

if "history" not in st.session_state: st.session_state.history = []

# --- 2. ترسانة الوظائف الميدانية (صوت، تلغرام، بحث) ---

def play_voice(text):
    """تحويل النص إلى صوت مسموع"""
    clean_text = re.sub(r'[^\w\s]', '', text)
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{clean_text[:300]}');
        msg.lang = 'ar-SA';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

def send_to_telegram(message):
    """إرسال التقرير إلى تلغرام راشد"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        return True
    except: return False

def advanced_radar(query):
    """البحث الميداني (رادار تافيلي)"""
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search = tavily.search(query=query, search_depth="advanced")
        return search['results'][0]['content']
    except: return "الرادار لم يرصد بيانات جديدة."

# --- 3. تصميم واجهة Gemini (مطابق لصورك) ---

with st.sidebar:
    st.markdown(f"<h1 style='color: #FF0000;'>⚡ الرعد</h1>", unsafe_allow_html=True)
    st.write(f"مرحباً **أبو سعود**")
    
    # ميزات سريعة (من صورتك رقم 3)
    st.button("🎨 إنشاء صورة", use_container_width=True)
    st.button("📚 ساعدني في التعلّم", use_container_width=True)
    
    st.divider()
    # المحادثات السابقة (من صورتك رقم 7)
    with st.expander("💬 السجل الاستخباراتي", expanded=True):
        st.caption("شبكة Molthub")
        st.caption("تحليل إبستين")
        st.caption("سعر الذهب بالأردن")
    
    st.divider()
    # ملاحظات سرية (من صورتك رقم 1)
    st.markdown("### 🕵️ ملاحظات سرية")
    st.text_area("سجل هنا...", height=100, key="v20_notes")

# --- 4. رصف الأزرار الأفقية (إصلاح صورتك رقم 11) ---
def show_action_bar(idx, text):
    cols = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 10])
    if cols[0].button("👍", key=f"lk_{idx}"): st.toast("تم")
    if cols[1].button("👎", key=f"dk_{idx}"): st.toast("تم")
    if cols[2].button("🔄", key=f"re_{idx}"): st.rerun()
    if cols[3].button("📤", key=f"tg_{idx}"): 
        if send_to_telegram(text): st.success("أُرسل لتلغرام")
    if cols[4].button("📋", key=f"cp_{idx}"): st.success("تم النسخ")
    if cols[5].button("🔊", key=f"vc_{idx}"): play_voice(text)
    cols[6].button("⋮", key=f"mr_{idx}")

# --- 5. محرك العمليات ---

for i, m in enumerate(st.session_state.history):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant": show_action_bar(i, m["content"])

# مركز الملحقات (أفقي)
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.write("📓 NotebookLM")
up_img = c3.file_uploader("🖼️ صور", type=['png', 'jpg'], label_visibility="collapsed")
c4.button("📷 كاميرا")

if inp := st.chat_input("أصدر أوامرك يا قائد أبو سعود..."):
    st.session_state.history.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    
    with st.chat_message("assistant"):
        # تشغيل الرادار تلقائياً للبحث
        context = advanced_radar(inp)
        
        client = Groq(api_key=GROQ_KEY)
        # دمج الشخصية والبحث
        sys_msg = f"أنت الرعد نسخة Gemini لراشد. التوقيت {clock_face}. السياق: {context}"
        
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": inp}]
        )
        final_res = resp.choices[0].message.content
        st.markdown(final_res)
        show_action_bar(len(st.session_state.history), final_res)
        st.session_state.history.append({"role": "assistant", "content": final_res})
