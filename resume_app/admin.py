from django.contrib import admin
from .models import Education, Resume, Experience, ResumeTemplate, Skill, Profile, Announcement

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(Announcement)
admin.site.register(Education)
admin.site.register(ResumeTemplate)