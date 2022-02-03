from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for jobprofile.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    is_manager = models.BooleanField(_("manager status"), default=False)
    is_agent = models.BooleanField(_("agent status"), default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Manager(models.Model):
    sector = models.CharField(_("Sector"), max_length=50)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="manager"
    )

    def __str__(self):
        return f"{self.user} Manager"


class Agent(models.Model):
    code = models.CharField(_("Code"), max_length=10)
    manager = models.ForeignKey(
        "Manager",
        on_delete=models.CASCADE,
        verbose_name="Manager Id",
        related_name="agent",
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="agent"
    )

    def __str__(self):
        return f"{self.user} Agent"
