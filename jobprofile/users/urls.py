from django.urls import path

from jobprofile.users.views import (
    AgentListView,
    AssignAgentView,
    CandidateRequestLike,
    ManagerCreateView,
    ManagerListView,
    UserCreateView,
    candidateRequestView,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"

urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("user/create/", view=UserCreateView.as_view(), name="user-create"),
    path("agent/assign/", view=AssignAgentView.as_view(), name="agent-assign"),
    path("agent/list/", view=AgentListView.as_view(), name="agent-list"),
    path("manager/create/", view=ManagerCreateView.as_view(), name="manager-create"),
    path("manager/list/", view=ManagerListView.as_view(), name="manager-list"),
    path("candidate", view=candidateRequestView.as_view(), name="candidate-list"),
    path(
        "candidate/update/<int:pk>",
        view=CandidateRequestLike.as_view(),
        name="candidate-like",
    ),
]
