"""
🔧 أدوات CrewAI المتقدمة
أدوات متطورة للبحث والتحليل
"""

from crewai_tools import tool
from duckduckgo_search import DDGS
from youtube_search import YoutubeSearch
import requests
from bs4 import BeautifulSoup
import json
from typing import Optional

# أداة البحث في الويب
@tool("web_search")
def web_search(query: str, max_results: int = 5) -> str:
    """
    البحث في الويب باستخدام DuckDuckGo
    يجلب الروابط والملخصات
    """
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=max_results)
        
        if not results:
            return "❌ لم يتم العثور على نتائج"
        
        search_results = "🔍 نتائج البحث:\n\n"
        for i, result in enumerate(results, 1):
            search_results += f"{i}. **{result['title']}**\n"
            search_results += f"   🔗 الرابط: {result['href']}\n"
            search_results += f"   📝 الملخص: {result['body']}\n\n"
        
        return search_results
    except Exception as e:
        return f"❌ خطأ في البحث: {str(e)}"

# أداة البحث عن فيديوهات YouTube
@tool("youtube_search")
def youtube_search(query: str, max_results: int = 5) -> str:
    """
    البحث عن فيديوهات YouTube
    يجلب عناوين الفيديوهات والروابط
    """
    try:
        results = YoutubeSearch(query, max_results=max_results).to_dict()
        
        if not results:
            return "❌ لم يتم العثور على فيديوهات"
        
        videos = "🎥 فيديوهات YouTube:\n\n"
        for i, video in enumerate(results, 1):
            video_id = video.get('id', '')
            title = video.get('title', 'بدون عنوان')
            channel = video.get('channel', 'قناة غير معروفة')
            duration = video.get('duration', 'مدة غير معروفة')
            
            videos += f"{i}. **{title}**\n"
            videos += f"   📺 القناة: {channel}\n"
            videos += f"   ⏱️ المدة: {duration}\n"
            videos += f"   🔗 الرابط: https://www.youtube.com/watch?v={video_id}\n\n"
        
        return videos
    except Exception as e:
        return f"❌ خطأ في البحث عن الفيديوهات: {str(e)}"

# أداة استخراج محتوى الصفحة
@tool("extract_page_content")
def extract_page_content(url: str) -> str:
    """
    استخراج محتوى الصفحة من رابط معين
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # إزالة الأكواد والتنسيقات غير المهمة
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return f"📄 محتوى الصفحة:\n\n{text[:2000]}..."
    except Exception as e:
        return f"❌ خطأ في استخراج المحتوى: {str(e)}"

# أداة التحليل المتقدم
@tool("advanced_analysis")
def advanced_analysis(content: str, analysis_type: str = "summary") -> str:
    """
    تحليل متقدم للمحتوى
    """
    try:
        if analysis_type == "summary":
            return f"📊 ملخص المحتوى:\n{content[:500]}..."
        elif analysis_type == "keywords":
            words = content.split()
            keywords = sorted(set(words), key=lambda x: words.count(x), reverse=True)[:10]
            return f"🔑 الكلمات المفتاحية:\n{', '.join(keywords)}"
        else:
            return f"📈 تحليل شامل:\n{content[:300]}..."
    except Exception as e:
        return f"❌ خطأ في التحليل: {str(e)}"

# أداة الترجمة والصياغة
@tool("format_response")
def format_response(content: str, language: str = "ar") -> str:
    """
    صياغة الإجابة بطريقة احترافية
    """
    try:
        formatted = f"""
        ✨ **الإجابة المصاغة احترافياً:**
        
        {content}
        
        ---
        ✅ تم معالجة الطلب بنجاح
        """
        return formatted
    except Exception as e:
        return f"❌ خطأ في الصياغة: {str(e)}"
