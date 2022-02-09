from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image


class CandidateProfile(models.Model):
    PROFILE_STATE = (
        ("new", _("NEW")),
        ("active", _("ACTIVE")),
        ("rejected", _("REJECTED")),
        ("assigned", _("ASSIGNED")),
        ("closed", _("CLOSED")),
    )

    REF_MEDIA = (("agent", _("AGENT")), ("other", _("SOCIAL")))
    name = models.CharField(_("Your Name"), max_length=100)
    phone_number = models.CharField(_("Mobile No"), max_length=10)
    birth_date = models.DateField(_("Date Of Birth"), auto_now=False)
    email = models.EmailField(_("Mail Id"), unique=True)
    address = models.TextField(_("Address"))
    profile_state = models.CharField(
        _("Profile State"), max_length=80, choices=PROFILE_STATE, default="new"
    )
    reference = models.CharField(
        _("Our Reference"), max_length=80, choices=REF_MEDIA, default="other"
    )
    profile_pic = models.ImageField(_("Your profile Pic"))
    reference_details = models.CharField(_("Reference Provider"), max_length=30)
    language = models.TextField(_("Language Know"))

    def __str__(self):
        return f"{self.name} Profile!"

    def save(self):
        super().save()
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (50, 50)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


class Study(models.Model):
    name = models.CharField(_("Institute Name"), max_length=70)
    standard = models.CharField(_("Standard Name"), max_length=100)
    percentage = models.FloatField(_("Percentage"))
    year = models.DateField(_("Year"))
    candidate = models.ForeignKey(
        "CandidateProfile", on_delete=models.CASCADE, related_name="study"
    )
    course = models.TextField(_("Special Course"), null=True)
    cgpa = models.FloatField(_("Your CGPA"), null=True)

    def __str__(self):
        return f"{self.name} Study"


class Experience(models.Model):
    company = models.CharField(_("Company Name"), max_length=60)
    latter = models.ImageField(_("Company Experience Latter"), max_length=60, null=True)
    start_date = models.DateField(_("Join Date"), auto_now=False)
    end_date = models.DateField(_("End Date"), auto_now=False)
    role = models.CharField(_("Previous Company Role"), max_length=80, null=True)
    New_role = models.CharField(
        _("Looking For Role"), default="developer", max_length=80
    )
    candidate = models.ForeignKey(
        "CandidateProfile", on_delete=models.CASCADE, related_name="experience"
    )
    description = models.TextField(_("Job Description"))

    def __str__(self):
        return f"{self.company} Company"


class Skill(models.Model):
    candidate = models.ForeignKey(
        "CandidateProfile", on_delete=models.CASCADE, related_name="can_skill"
    )
    skill_level = models.IntegerField(
        _("Skill Level"),
        null=True,
    )
    technical_skill = models.TextField(_("Technical Skills"))
    soft_skill = models.TextField(_("Soft Skill"))
    project = models.TextField(_("Project Details"))

    def __str__(self):
        return f"{self.skill} Technical"
