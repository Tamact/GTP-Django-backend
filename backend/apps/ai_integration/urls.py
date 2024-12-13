from django.urls import path
from .views import GenerateQuestionnaireView, CategorizeSkillsView, DetectAIGeneratedTextView, AnalyzeTextStyleView

urlpatterns = [
    path('generate_questionnaire/', GenerateQuestionnaireView.as_view(), name='generate-questionnaire'),
    path('categorize_skills/', CategorizeSkillsView.as_view(), name='categorize-skills'),
    path('detect_ai_generated_text/', DetectAIGeneratedTextView.as_view(), name='detect-ai-generated-text'),
    path('analyze_text_style/', AnalyzeTextStyleView.as_view(), name='analyze-text-style'),
]