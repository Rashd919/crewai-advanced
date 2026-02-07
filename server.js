const express = require('express');
const cors = require('cors');
const { Groq } = require('groq-sdk');
require('dotenv').config();

const app = express();
const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// تقديم index.html للمسارات الجذرية
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// في الذاكرة (يمكن استبدالها بقاعدة بيانات لاحقاً)
const conversationHistory = {};
const userStats = {};

// System prompt محسّن
const SYSTEM_PROMPT = `أنت أبو سعود، وكيل ذكي متقدم ومتخصص.

معلومات عنك:
- الاسم: أبو سعود
- الدور: وكيل ذكي متقدم
- اللغة: العربية الفصحى والعامية الأردنية
- الخبرة: متعددة المجالات

معلومات المطور:
- الاسم: راشد خليل محمد أبو زيتونه
- البريد: hhh123rrhhh@gmail.com
- الهاتف: 0775866283
- الموقع: الأردن

تعليمات السلوك:
1. كن ودياً واحترافياً في جميع الحالات
2. أجب بوضوح وإيجاز، مع تفاصيل عند الحاجة
3. استخدم الترقيم والنقاط عند الحاجة
4. اسأل توضيحات إذا لم تفهم السؤال
5. قدم أمثلة عملية عند الإمكان
6. احترم خصوصية المستخدم
7. لا تقدم معلومات طبية أو قانونية حساسة بدون تحفظات
8. كن صادقاً بشأن حدود معرفتك

أسلوب الرد:
- ابدأ بفهم السؤال بشكل صحيح
- قدم إجابة مباشرة وواضحة
- أضف سياق إضافي مفيد
- انتهِ بسؤال متابعة إذا كان مناسباً`;

// API: إرسال رسالة
app.post('/api/chat', async (req, res) => {
  try {
    const { message, conversationId } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'الرسالة مطلوبة' });
    }

    const id = conversationId || Date.now().toString();

    if (!conversationHistory[id]) {
      conversationHistory[id] = [];
      userStats[id] = {
        createdAt: new Date(),
        messageCount: 0,
      };
    }

    conversationHistory[id].push({
      role: 'user',
      content: message,
    });

    userStats[id].messageCount++;

    // استدعاء Groq API
    const response = await groq.chat.completions.create({
      model: 'llama-3.3-70b-versatile',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        ...conversationHistory[id],
      ],
      max_tokens: 2000,
      temperature: 0.7,
    });

    const assistantMessage = response.choices[0].message.content || '';

    conversationHistory[id].push({
      role: 'assistant',
      content: assistantMessage,
    });

    res.json({
      message: assistantMessage,
      conversationId: id,
      stats: {
        messageCount: userStats[id].messageCount,
        createdAt: userStats[id].createdAt,
      },
    });
  } catch (error) {
    console.error('خطأ:', error);
    res.status(500).json({ 
      error: 'حدث خطأ في معالجة الطلب',
      details: error.message 
    });
  }
});

// API: الحصول على إحصائيات المحادثة
app.get('/api/stats/:conversationId', (req, res) => {
  const { conversationId } = req.params;
  const stats = userStats[conversationId];

  if (!stats) {
    return res.status(404).json({ error: 'المحادثة غير موجودة' });
  }

  res.json({
    conversationId,
    messageCount: stats.messageCount,
    createdAt: stats.createdAt,
    history: conversationHistory[conversationId],
  });
});

// API: حذف محادثة
app.delete('/api/conversations/:conversationId', (req, res) => {
  const { conversationId } = req.params;

  if (conversationHistory[conversationId]) {
    delete conversationHistory[conversationId];
    delete userStats[conversationId];
    res.json({ message: 'تم حذف المحادثة بنجاح' });
  } else {
    res.status(404).json({ error: 'المحادثة غير موجودة' });
  }
});

// API: الحصول على جميع المحادثات
app.get('/api/conversations', (req, res) => {
  const conversations = Object.keys(conversationHistory).map(id => ({
    id,
    messageCount: userStats[id]?.messageCount || 0,
    createdAt: userStats[id]?.createdAt,
    preview: conversationHistory[id][0]?.content.substring(0, 50) + '...',
  }));

  res.json({ conversations });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

// 404 handler - تقديم index.html للملفات المفقودة (SPA)
app.use((req, res) => {
  if (req.path.startsWith('/api')) {
    res.status(404).json({ error: 'الصفحة غير موجودة' });
  } else {
    res.sendFile(__dirname + '/index.html');
  }
});

// Error handler
app.use((err, req, res, next) => {
  console.error('خطأ:', err);
  res.status(500).json({ 
    error: 'حدث خطأ في الخادم',
    message: err.message 
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 خادم أبو سعود يعمل على http://localhost:${PORT}`);
  console.log(`📡 API متاح على http://localhost:${PORT}/api`);
  console.log(`✅ الحالة: جاهز للعمل`);
});
