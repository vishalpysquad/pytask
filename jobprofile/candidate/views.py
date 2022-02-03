from django.views.generic import CreateView

from .forms import CandidateProfileForm


class CreateCandidateProfileView(CreateView):

    template_name = "candidate/candidate_form.html"
    success_url = "/"
    form_class = CandidateProfileForm
