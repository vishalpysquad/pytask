from django.contrib import admin

from jobprofile.candidate.models import CandidateProfile, Experience, Skill, Study

admin.site.register(CandidateProfile)
admin.site.register(Study),
admin.site.register(Experience),
admin.site.register(Skill),
