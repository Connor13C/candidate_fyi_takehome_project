from django.contrib import admin
from candidate_fyi_takehome_project.interviews.models import InterviewTemplate, Interviewer

# Register your models here.
admin.site.register(InterviewTemplate)
admin.site.register(Interviewer)
