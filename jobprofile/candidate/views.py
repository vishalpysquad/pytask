from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from .forms import CandidateExperienceForm, CandidateProfileForm, CandidateStudyForm


class CreateCandidateProfileView(SuccessMessageMixin, CreateView):

    template_name = "candidate/candidate_form.html"
    success_url = reverse_lazy("home")
    form_class = CandidateProfileForm
    success_message = _("Information successfully Added")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["candidate_experience"] = CandidateExperienceForm(self.request.POST)
        context["candidate_study"] = CandidateStudyForm(self.request.POST)
        return context

    def form_valid(self, form):
        candidate = form.save()
        candidate_experience = self.get_form(form_class=CandidateExperienceForm)
        candidate_experience.instance.candidate_id = candidate.id
        candidate_study = self.get_form(form_class=CandidateStudyForm)
        candidate_study.instance.candidate_id = candidate.id
        if candidate_experience.is_valid() and candidate_study.is_valid():
            candidate_experience.save()
            candidate_study.save()
        return super().form_valid(form)
