"""
👥 فريق CrewAI المتقدم
نظام الوكلاء الذكيين المتكامل
"""

from crewai import Crew, Process
from agents import super_researcher, technical_analyst, project_manager
from tasks import create_research_task, create_analysis_task, create_coordination_task
from dotenv import load_dotenv
import os

load_dotenv()

class AdvancedCrew:
    """فريق CrewAI المتقدم"""
    
    def __init__(self):
        """تهيئة الفريق"""
        self.crew = None
        self.research_results = None
        self.analysis_results = None
    
    def create_crew(self, query: str):
        """
        إنشاء فريق للعمل على استعلام معين
        """
        # إنشاء المهام
        research_task = create_research_task(query)
        analysis_task = create_analysis_task("")
        coordination_task = create_coordination_task("", "")
        
        # إنشاء الفريق
        self.crew = Crew(
            agents=[super_researcher, technical_analyst, project_manager],
            tasks=[research_task, analysis_task, coordination_task],
            verbose=True,
            process=Process.hierarchical,
            manager_agent=project_manager
        )
        
        return self.crew
    
    def execute(self, query: str) -> str:
        """
        تنفيذ الفريق على استعلام معين
        """
        try:
            # إنشاء الفريق
            crew = self.create_crew(query)
            
            # تنفيذ الفريق
            result = crew.kickoff()
            
            return result
        except Exception as e:
            return f"❌ خطأ في تنفيذ الفريق: {str(e)}"
    
    def execute_research_only(self, query: str) -> str:
        """
        تنفيذ البحث فقط
        """
        try:
            task = create_research_task(query)
            crew = Crew(
                agents=[super_researcher],
                tasks=[task],
                verbose=True,
                process=Process.sequential
            )
            result = crew.kickoff()
            self.research_results = result
            return result
        except Exception as e:
            return f"❌ خطأ في البحث: {str(e)}"
    
    def execute_analysis_only(self, research_results: str) -> str:
        """
        تنفيذ التحليل فقط
        """
        try:
            task = create_analysis_task(research_results)
            crew = Crew(
                agents=[technical_analyst],
                tasks=[task],
                verbose=True,
                process=Process.sequential
            )
            result = crew.kickoff()
            self.analysis_results = result
            return result
        except Exception as e:
            return f"❌ خطأ في التحليل: {str(e)}"
    
    def execute_full_pipeline(self, query: str) -> dict:
        """
        تنفيذ خط أنابيب كامل
        """
        try:
            # المرحلة 1: البحث
            print("🔍 جاري البحث...")
            research_results = self.execute_research_only(query)
            
            # المرحلة 2: التحليل
            print("📊 جاري التحليل...")
            analysis_results = self.execute_analysis_only(research_results)
            
            # المرحلة 3: التنسيق
            print("📋 جاري التنسيق...")
            coordination_task = create_coordination_task(research_results, analysis_results)
            crew = Crew(
                agents=[project_manager],
                tasks=[coordination_task],
                verbose=True,
                process=Process.sequential
            )
            final_result = crew.kickoff()
            
            return {
                "status": "✅ نجح",
                "research": research_results,
                "analysis": analysis_results,
                "final_result": final_result
            }
        except Exception as e:
            return {
                "status": f"❌ خطأ: {str(e)}",
                "research": None,
                "analysis": None,
                "final_result": None
            }

# إنشاء نسخة من الفريق
advanced_crew = AdvancedCrew()

def get_crew():
    """الحصول على الفريق"""
    return advanced_crew

def execute_query(query: str) -> str:
    """تنفيذ استعلام"""
    return advanced_crew.execute(query)

def execute_research(query: str) -> str:
    """تنفيذ بحث"""
    return advanced_crew.execute_research_only(query)

def execute_analysis(research_results: str) -> str:
    """تنفيذ تحليل"""
    return advanced_crew.execute_analysis_only(research_results)

def execute_full(query: str) -> dict:
    """تنفيذ خط أنابيب كامل"""
    return advanced_crew.execute_full_pipeline(query)
