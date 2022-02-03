from django import forms

from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = [
            "name",
            "phone_number",
            "email",
            "birth_date",
            "reference",
            "address",
            "profile_pic",
            "reference",
            "reference_details",
            "language",
        ]
        widgets = {"birth_date": forms.DateInput()}
