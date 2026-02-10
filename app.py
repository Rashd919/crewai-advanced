def ask_thunder(prompt):
    cold_sys = "أنت 'الرعد'. مطورك راشد أبو سعود. رد ببرود وكفاءة."
    
    # التأكد من وجود المفاتيح قبل المحاولة
    if not GROQ_KEY:
        return "🚨 خلل أمني: مفتاح GROQ غير موجود في Secrets.", "ERROR"

    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": cold_sys}, {"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content, "Groq (Llama 3)"
    except Exception as e:
        # إذا فشل Groq، سيخبرنا بالسبب الحقيقي
        error_msg = str(e)
        if "401" in error_msg:
            return "❌ المفتاح الذي أدخلته (API Key) غير صالح أو منتهي.", "AUTH_ERROR"
        elif "429" in error_msg:
            return "⏳ حصار الكوتا: انتظر 60 ثانية للمناورة.", "RATE_LIMIT"
        
        # محاولة أخيرة عبر Gemini
        try:
            client_gem = genai.Client(api_key=GEMINI_KEY)
            res = client_gem.models.generate_content(model="gemini-1.5-flash", contents=prompt)
            return res.text, "Gemini (Backup)"
        except Exception as e2:
            return f"🚨 انهيار شامل. الخطأ: {str(e2)}", "CRITICAL_FAIL"
