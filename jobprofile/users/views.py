from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

from jobprofile.candidate.models import CandidateProfile

from .forms import UserRegisatrtionForm
from .models import Agent, Manager

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name", "is_manager"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserTypeCheckMixin(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin):
    def test_func(self):
        return (
            True
            if self.request.user.is_manager or self.request.user.is_superuser
            else False
        )


class UserCreateView(UserTypeCheckMixin, CreateView):

    form_class = UserRegisatrtionForm
    template_name = "pages/registration_form.html"
    model = User
    success_message = _("User Create successfully")

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)


class AssignAgentView(UserTypeCheckMixin, CreateView):

    model = Agent
    template_name = "pages/assign_agent.html"
    fields = ["code", "user"]
    success_url = reverse_lazy("home")
    success_message = _("Agent Assign Successfully ")

    def form_valid(self, form):
        form.instance.manager_id = self.request.user.manager.id
        form.save()
        return super(AssignAgentView, self).form_valid(form)


class AgentListView(UserTypeCheckMixin, ListView):

    model = Agent
    template_name = "pages/agent_list.html"

    def get_queryset(self):
        agents_list = Agent.objects.filter(manager_id=self.request.user.manager.id)
        search_list = self.request.GET.get("search_list")
        if search_list:
            agents_list = Agent.objects.filter(code__icontains=search_list)
            return agents_list
        return agents_list


class ManagerCreateView(UserTypeCheckMixin, CreateView):

    model = Manager
    template_name = "pages/manager_form.html"
    fields = ["user", "sector"]
    success_url = "/"
    success_message = _("Manager Create successfully.")
    context = User.objects.filter(is_manager="True")

    def test_func(self):
        return True if self.request.user.is_superuser else False


class ManagerListView(UserTypeCheckMixin, ListView):

    model = Manager
    template_name = "pages/manager_list.html"

    def test_func(self):
        return True if self.request.user.is_superuser else False


class candidateRequestView(UserTypeCheckMixin, ListView):

    model = CandidateProfile
    template_name = "pages/candidate_request.html"

    def test_func(self):
        return (
            True
            if self.request.user.is_manager or self.request.user.agent.code
            else False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_manager:
            context["other"] = CandidateProfile.objects.filter(reference="other")
            context["candidates"] = CandidateProfile.objects.filter(
                reference_details__in=self.request.user.manager.agent.all().values_list(
                    "code", flat=True
                )
            )
            return context
        elif self.request.user.is_agent:
            context["candidates"] = CandidateProfile.objects.filter(
                reference_details=self.request.user.agent.code
            )
        return context


class CandidateRequestLike(UserTypeCheckMixin, UpdateView):

    model = CandidateProfile
    template_name = "pages/update_profile.html"
    fields = ["profile_state"]
    success_url = reverse_lazy("users:candidate-list")
    success_message = _("Profile Updated successfully")

    def test_func(self):
        return True if self.request.user.is_manager else False
