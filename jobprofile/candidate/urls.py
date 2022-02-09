from django.urls import path

from jobprofile.candidate.views import CreateCandidateProfileView

app_name = "candidate"

urlpatterns = [
    path("candidate/", view=CreateCandidateProfileView.as_view(), name="candidate"),
]
