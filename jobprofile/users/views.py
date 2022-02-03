from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

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


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    form_class = UserRegisatrtionForm
    template_name = "pages/registration_form.html"
    model = User

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)

    def test_func(self):
        return (
            True
            if self.request.user.is_manager or self.request.user.is_superuser
            else False
        )


class AssignAgentView(CreateView):

    model = Agent
    template_name = "pages/assign_agent.html"
    fields = ["code", "user"]
    success_url = "/"


class AgentListView(ListView):

    model = Agent
    template_name = "pages/agent_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["agents"] = Agent.objects.filter(
            manager_id=self.request.user.manager.id
        )
        return context

    def get_queryset(self):
        agents_list = Agent.objects.all()
        search_list = self.request.GET.get("search_list")
        if search_list:
            agents_list = Agent.objects.filter(code__icontains=search_list)
            return agents_list
        return agents_list


class ManagerCreateView(CreateView):

    model = Manager
    template_name = "pages/manager_form.html"
    fields = ["user", "sector"]
    success_url = "/"
    context = User.objects.filter(is_manager="True")


class ManagerListView(ListView):

    model = Manager
    template_name = "pages/manager_list.html"
