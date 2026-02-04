# 🚀 دليل التثبيت والتشغيل - CrewAI Advanced

## المتطلبات
- Python 3.8 أو أحدث
- pip أو conda
- Git

## خطوات التثبيت

### 1. استنساخ المشروع
```bash
git clone https://github.com/Rashd919/crewai-advanced.git
cd crewai-advanced
```

### 2. إنشاء بيئة افتراضية (اختياري لكن موصى به)

**على Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**على macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة
أنشئ ملف `.env` في المجلد الرئيسي:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo
```

### 5. تشغيل التطبيق
```bash
streamlit run app.py
```

التطبيق سيفتح تلقائياً في المتصفح على: `http://localhost:8501`

## استكشاف الأخطاء

### خطأ: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### خطأ: "OPENAI_API_KEY not found"
تأكد من وجود ملف `.env` وأنه يحتوي على مفتاح API الصحيح

### خطأ: "Port 8501 is already in use"
```bash
streamlit run app.py --server.port 8502
```

## الملفات الرئيسية

- `app.py` - واجهة Streamlit الرئيسية
- `crew.py` - فريق CrewAI والتنفيذ
- `agents.py` - تعريف الوكلاء الذكيين
- `tasks.py` - تعريف المهام
- `tools.py` - الأدوات المخصصة
- `requirements.txt` - المكتبات المطلوبة

## الدعم

للمساعدة والاستفسارات:
- 📧 البريد: your.email@example.com
- 🐙 GitHub: https://github.com/Rashd919/crewai-advanced
