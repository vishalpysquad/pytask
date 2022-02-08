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
        context["form1"] = CandidateExperienceForm(self.request.POST)
        context["form2"] = CandidateStudyForm(self.request.POST)
        return context

    def form_valid(self, form):
        candidate = form.save()
        form1 = self.get_form(form_class=CandidateExperienceForm)
        form1.instance.candidate_id = candidate.id
        form2 = self.get_form(form_class=CandidateStudyForm)
        form2.instance.candidate_id = candidate.id
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
        return super().form_valid(form)
