from django.contrib import admin
from django.urls import path
from .views import EducationCreateView, ExperienceCreateView, SkillCreateView, home, export_resume_pdf, register, resume_create, resume_preview, user_login, user_logout, profile, resume_list, resume_list_all
from .views import announcement_list, template_catalog
from .views import ResumeUpdateView
urlpatterns = [
    path('resume/<int:pk>/pdf/', export_resume_pdf, name='export_resume_pdf'),
    path('', home, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('resume/create/', resume_create, name='resume_create'),
    path('resume/<int:pk>/edit/', ResumeUpdateView.as_view(), name='resume_edit'),
    path('resume/<int:resume_pk>/education/', EducationCreateView.as_view(), name='education_add'),
    path('resume/<int:resume_pk>/experience/', ExperienceCreateView.as_view(), name='experience_add'),
    path('resume/<int:resume_pk>/skills/', SkillCreateView.as_view(), name='skill_add'),
    path('resumes/', resume_list, name='resume-list'),
    path('resumes/all/', resume_list_all, name='resume-list-all'),
    path('announcements/', announcement_list, name='announcement-list'),
    path('templates/', template_catalog, name='template_catalog'),
    path('resume/<int:pk>/preview/', resume_preview, name='resume_preview'),

]