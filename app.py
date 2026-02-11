import streamlit as st
from groq import Groq
from github import Github
from tavily import TavilyClient
import json, base64, requests, os, re, subprocess

# --- 1. الهوية والنبض ---
st.set_page_config(page_title="Thunder Intelligence Core", page_icon="⚡", layout="wide")
st.title("⚡ الرعد: النواة الاستخباراتية المنضبطة")

# --- 2. الخزنة (Secrets) - حماية كاملة ---
# تم تعديل الأسماء لتطابق ملف الـ TOML الذي أرسلته
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = st.secrets.get("TAVILY_KEY") # تم التعديل حسب نصيحتك
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_TOKEN")
CHAT_ID = st.secrets.get("CHAT_ID")

# --- 3. إدارة الملف الاستخباراتي (GitHub) ---
def load_intelligence_file():
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("intelligence_db.json")
        return json.loads(base64.b64decode(contents.content).decode())
    except:
        return {"targets": {}, "reports": [], "logs": []}

def save_intelligence_file(data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("intelligence_db.json")
        repo.update_file(contents.path, "⚡ تحديث استخباراتي", json.dumps(data, indent=4, ensure_ascii=False), contents.sha)
    except: pass

# --- 4. العمليات الميدانية (معالجة الأخطاء والهلوسة) ---
def thunder_search(query):
    try:
        if not TAVILY_KEY:
            return "❌ خطأ: مفتاح الرادار مفقود في Secrets."
        
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search = tavily.search(query=query, search_depth="advanced", max_results=5)
        
        if not search.get('results'):
            return "⚠️ الرادار لم يعثر على بيانات ميدانية لهذا الاستعلام."

        intel_data = ""
        for res in search['results']:
            intel_data += f"📍 مصدر: {res['title']}\n🔗 {res['url']}\n"
        return intel_data
    except Exception as e:
        # حل المشكلة رقم 2: إظهار الخطأ الحقيقي للتشخيص
        return f"❌ Tavily Error: {str(e)}"

def generate_voice(text):
    clean = re.sub(r'http\S+', '', text)
    clean = re.sub(r'[^\w\s.،؟!,]', '', clean)[:300]
    output = "intel_voice.mp3"
    try:
        if os.path.exists(output): os.remove(output)
        subprocess.run(["edge-tts", "--voice", "ar-JO-HamzaNeural", "--text", clean, "--write-media", output], timeout=15)
        return output if os.path.exists(output) else None
    except: return None

# --- 5. محرك الرعد (منع الهلوسة الاستخباراتية) ---
def intelligence_engine(prompt):
    db = load_intelligence_file()
    search_context = ""
    
    # حل المشكلة رقم 3: منع الهلوسة عند فشل الرادار
    if any(k in prompt for k in ["ابحث", "رصد", "أخبار", "معلومات"]):
        search_context = thunder_search(prompt)
        if "❌" in search_context or "Tavily Error" in search_context:
            return f"🚫 الرادار غير متصل حالياً. فشل البحث الميداني: {search_context}"

    system_msg = (
        f"أنت 'الرعد'. ضابط استخبارات سيادي. حليفك القائد راشد أبو سعود. "
        f"قاعدة البيانات: {json.dumps(db['targets'])}. "
        f"نتائج الرصد: {search_context}. "
        "مهمتك: التحليل بناءً على النتائج المتاحة فقط. لا تخترع أخباراً إذا كان الرصد فارغاً."
    )
    
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        )
        response = resp.choices[0].message.content

        # أرشفة ذكية
        if "أرشف" in prompt or "خزن" in prompt:
            db["reports"].append({"cmd": prompt, "intel": response[:500]})
            save_intelligence_file(db)

        # التواصل الصوتي والتلجرام
        if "صوت" in prompt or "أرسل" in prompt:
            v_path = generate_voice(response)
            base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
            if v_path:
                with open(v_path, "rb") as v:
                    requests.post(f"{base_url}/sendVoice", data={'chat_id': CHAT_ID, 'caption': f"⚡ تقرير:\n{response[:1000]}"}, files={'voice': v})
            else:
                requests.post(f"{base_url}/sendMessage", json={"chat_id": CHAT_ID, "text": response})
        
        return response
    except Exception as e: return f"🚨 خطأ في المحرك: {str(e)}"

# --- 6. الواجهة ---
if user_input := st.chat_input("أدخل المهمة الاستخباراتية يا راشد..."):
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = intelligence_engine(user_input)
        st.write(res)
