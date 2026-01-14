import django
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from io import BytesIO
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Education, Experience, Resume, Announcement, Skill
from .forms import EducationForm, ExperienceForm, SkillForm, UserRegisterForm, ProfileUpdateForm, ResumeForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Головна сторінка
def home(request):
    announcements = Announcement.objects.order_by('-created_at')[:3]
    resumes = Resume.objects.all()[:3]
    return render(request, 'resumes/base.html', {
        'announcements': announcements,
        'resumes': resumes
    })

def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("PDF generation error", status=500)

def export_resume_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    context = {'resume': resume}
    return render_to_pdf('resumes/pdf_template.html', context)

# Реєстрація
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'resumes/register.html', {'form': form})

# Вхід
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'resumes/login.html', {'form': form})

# Вихід
def user_logout(request):
    logout(request)
    return redirect('index')

# Профіль
@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'resumes/profile.html', {'p_form': p_form})

# Список резюме
@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

# Вивід списку резюме (аналог пост-ліста)
def resume_list_all(request):
    resumes = Resume.objects.all()
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

def announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'resumes/announcement_list.html', {'announcements': announcements})

# --- CRUD для Оголошень (Announcement) ---
@staff_member_required
def announcement_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Announcement.objects.create(title=title, content=content)
            messages.success(request, 'Оголошення створено!')
            return redirect('announcement_list')
        else:
            messages.error(request, 'Всі поля обовʼязкові!')
    return render(request, 'resumes/announcement_form.html')

@staff_member_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.content = request.POST.get('content')
        announcement.save()
        messages.success(request, 'Оголошення оновлено!')
        return redirect('announcement_list')
    return render(request, 'resumes/announcement_form.html', {'announcement': announcement})

@staff_member_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Оголошення видалено!')
        return redirect('announcement_list')
    return render(request, 'resumes/announcement_confirm_delete.html', {'announcement': announcement})

# --- CRUD для Резюме (Resume) ---
@login_required
def resume_create(request):
    form = ResumeForm()
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            resume =form.save()
            messages.success(request, 'Резюме створено!')
            return redirect('education_add', resume_pk=resume.pk)
        else:
            messages.error(request, 'Всі поля обовʼязкові!')
    return render(request, 'resumes/resume_form.html', {'form': form})

class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/resume_form.html'
    success_url = '/resumes/'

class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'resumes/education_form.html'

    def form_valid(self, form):
       
        form.instance.resume = get_object_or_404(Resume, pk=self.kwargs['resume_pk'], user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        resume = get_object_or_404(Resume, pk=self.kwargs['resume_pk'], user=self.request.user)
        educations = Education.objects.filter(resume=resume)
        context['educations'] = educations
        context['resume'] = resume
        return context
    def get_success_url(self):
        return redirect('education_add', resume_pk=self.kwargs['resume_pk']).url

class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'resumes/experience_form.html'

    def form_valid(self, form):
       
        form.instance.resume = get_object_or_404(Resume, pk=self.kwargs['resume_pk'], user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        resume = get_object_or_404(Resume, pk=self.kwargs['resume_pk'], user=self.request.user)
        experiences = Experience.objects.filter(resume=resume)
        context['experiences'] = experiences
        context['resume'] = resume
        return context
    def get_success_url(self):
        return redirect('experience_add', resume_pk=self.kwargs['resume_pk']).url

class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'resumes/skill_form.html'

    def form_valid(self, form):
       
        form.instance.resume = get_object_or_404(Resume, pk=self.kwargs['resume_pk'], user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        resume = get_object_or_404(Resume, pk=self.kwargs['resume_pk'], user=self.request.user)
        skills = Skill.objects.filter(resume=resume)
        context['skills'] = skills
        context['resume'] = resume
        return context
    def get_success_url(self):
        return redirect('skill_add', resume_pk=self.kwargs['resume_pk']).url

@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Резюме видалено!')
        return redirect('resume_list')
    return render(request, 'resumes/resume_confirm_delete.html', {'resume': resume})

@login_required
def resume_clone(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.pk = None
    resume.title = f"Копія {resume.title}"
    resume.save()
    messages.success(request, 'Резюме скопійовано!')
    return redirect('resume_list')

@login_required
def resume_preview(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'resumes/resume_preview.html', {'resume': resume})

# --- Каталог шаблонів резюме з preview ---
def template_catalog(request):
    # Тестові шаблони для демонстрації
    templates = [
        {
            'pk': 1,
            'name': 'Класичний',
            'preview_url': '/static/resumes/static.css'  # замініть на реальне зображення
        },
        {
            'pk': 2,
            'name': 'Мінімалістичний',
            'preview_url': '/static/resumes/static.css'
        },
    ]
    return render(request, 'resumes/template_catalog.html', {'templates': templates})

# --- Розширене розділення ролей (user/admin) ---
def is_admin(user):
    return user.is_staff or user.is_superuser