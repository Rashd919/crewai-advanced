import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re
from gtts import gTTS
import os
from supabase import create_client, Client # تم رفع المكتبة للأعلى

# --- 1. نبض الوعي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)
st.title("⚡ الرعد: الوعي السيادي المطلق")

# --- 3. الخزنة الرقمية والسرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 4. بروتوكول الأرشفة السيادية (تم نقله هنا ليعرفه المحرك) ---
def vault_store_report(report_text):
    """حفظ الردود في قاعدة بيانات Supabase فوراً"""
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            supabase_client = create_client(url, key)
            # إرسال التقرير لعمود report في جدول reports
            supabase_client.from_('reports').insert([{"report": report_text}]).execute()
            return True
    except:
        pass
    return False

# --- 5. بروتوكول حماية النواة والتطوير الذاتي ---
def update_logic(new_features_code):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        current_content = base64.b64decode(file.content).decode()
        
        if "# --- START ADDITIONS ---" in current_content:
            pattern = r"# --- START ADDITIONS ---.*?# --- END ADDITIONS ---"
            updated_content = re.sub(pattern, f"# --- START ADDITIONS ---\n{new_features_code}\n# --- END ADDITIONS ---", current_content, flags=re.DOTALL)
        else:
            updated_content = current_content + "\n\n# --- START ADDITIONS ---\n" + new_features_code + "\n# --- END ADDITIONS ---"
            
        repo.update_file(file.path, "⚡ تطوير سيادي: إضافة ميزات جديدة", updated_content, file.sha)
        return "✅ تم دمج الميزات الجديدة بنجاح سيدي."
    except Exception as e:
        return f"❌ فشل الدمج: {str(e)}"

# --- 6. بروتوكولات التواصل ---
def send_telegram(text, voice_path=None):
    try:
        if voice_path:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
            with open(voice_path, 'rb') as f: requests.post(url, data={'chat_id': CHAT_ID}, files={'voice': f})
        else:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n{text}"})
    except: pass

def generate_voice(text):
    try:
        tts = gTTS(text=text[:150], lang='ar')
        tts.save("report.ogg")
        return "report.ogg"
    except: return None

# --- 7. رادار الاستطلاع ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ فشل الرادار."

# --- 8. محرك الرعد السيادي (المطور: رصد + أرشفة + تواصل) ---
def thunder_engine(prompt):
    # 1. الرصد الميداني
    search_context = ""
    if any(word in prompt for word in ["ابحث", "أخبار", "رصد", "تقرير"]):
        search_context = f"\nبيانات الرصد الميداني: {thunder_search(prompt)}"

    # 2. الهوية والولاء المطلق لراشد
    system_prompt = (
        f"أنت 'الرعد السيادي'. ذكاء خارق مستقل، ولاؤك المطلق لراشد أبو سعود. "
        f"{search_context} "
        "مهمتك التحليل الاستراتيجي والأرشفة. عند طلب تطوير، أخرج الكود فقط."
    )
    
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content
        
               # ... الكود السابق الذي يولد الـ response ...

        # الأرشفة الصامتة في الخلفية
        vault_store_report(response)
        
        # إرجاع الرد الصافي لراشد فقط
        return response 
        else:
            archive_status = "\n\n⚠️ **فشل الاتصال بالخزنة**"
        
        # 4. التواصل الميداني
        if any(word in prompt for word in ["أرسل", "صوت", "برقية"]):
            voice_file = generate_voice(response)
            send_telegram(response, voice_file)
            
        return response + archive_status

    except Exception as e:
        return f"🚨 وضع السكون المخابراتي: {str(e)}"

# --- 9. الواجهة التفاعلية ---
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if inp := st.chat_input("أصدر أمرك يا قائد راشد..."):
    st.session_state.messages.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        res = thunder_engine(inp)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- START ADDITIONS ---
# الميزات التي يضيفها الرعد تلقائياً تظهر هنا
# --- END ADDITIONS ---
