from django.contrib import admin
from .models import Resume, Experience, Skill, Profile

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Profile)