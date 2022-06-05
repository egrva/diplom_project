from django.urls import path
from django.views.generic import TemplateView

from api import views

urlpatterns = [

    path('analyze/student/<int:pk>/', views.student_analyze, name='student-analyze'),
    path('student-list/', views.student_list, name='student_list'),

    path('analyze-total/', views.analyze_total, name='analyze_total'),

    path('student-analyze/', views.student_list, name='student_list'),
    path('', TemplateView.as_view(template_name='index.html'), name='home')
]
