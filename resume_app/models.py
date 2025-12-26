from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes', verbose_name='Користувач')
    title = models.CharField(max_length=200, verbose_name='Назва')
    template = models.ForeignKey('ResumeTemplate', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Шаблон')
    summary = models.TextField(verbose_name='Про Мене')
    phonenumber = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефону')
    email = models.EmailField(blank=True, null=True, verbose_name='Електронна пошта')
    linkedin = models.URLField(blank=True, null=True, verbose_name='LinkedIn')
    github = models.URLField(blank=True, null=True, verbose_name='GitHub')
    website = models.URLField(blank=True, null=True, verbose_name='Вебсайт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення)')

class ResumeTemplate(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва шаблону')
    template_file = models.FileField(upload_to='resume_templates/', verbose_name='Файл шаблону')


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations',verbose_name='Резюме')
    institution = models.CharField(max_length=200, verbose_name='Навчальний заклад')
    degree = models.CharField(max_length=100, verbose_name='Ступінь')
    start_date = models.DateField(verbose_name='Дата початку')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата закінчення')
    description = models.TextField(blank=True, verbose_name='Опис')

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences', verbose_name='Резюме')
    position = models.CharField(max_length=100, verbose_name='Посада')
    company = models.CharField(max_length=100, verbose_name='Компанія')
    start_date = models.DateField(verbose_name='Дата початку')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата закінчення')
    description = models.TextField(blank=True, verbose_name='Опис')

class Skill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Початковий'),
        ('intermediate', 'Середній'),
        ('advanced', 'Просунутий'),
    ]
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills', verbose_name='Резюме')
    name = models.CharField(max_length=100, verbose_name='Назва навички')
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, verbose_name='Рівень')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Користувач')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, null=True, verbose_name='Біографія')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Місцезнаходження')

    def __str__(self):
        return f"{self.user.username} Profile"

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
