"""
URL configuration for resumebuilder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home, export_resume_pdf, register, user_login, user_logout, profile, resume_list, resume_list_all
from .views import announcement_list, template_catalog

urlpatterns = [
    path('resume/<int:pk>/pdf/', export_resume_pdf, name='export_resume_pdf'),
    path('', home, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('resumes/', resume_list, name='resume-list'),
    path('resumes/all/', resume_list_all, name='resume-list-all'),
    path('announcements/', announcement_list, name='announcement-list'),
    path('templates/', template_catalog, name='template_catalog'),
    path('admin/', admin.site.urls),
]