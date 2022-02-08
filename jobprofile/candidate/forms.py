from django import forms

from .models import CandidateProfile, Experience, Study


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
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}


class CandidateStudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ["name", "standard", "percentage", "year", "course", "CGPA"]
        widgets = {
            "year": forms.DateInput(attrs={"type": "date"}),
            "course": forms.TextInput(),
        }


class CandidateExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "company",
            "latter",
            "start_date",
            "end_date",
            "role",
            "New_role",
            "description",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    # def clean(self):
    #     import pdb
    #     pdb.set_trace()
    #     name = self.data.get("name")
    #     print(name)
    #     self.data
    #     return self.data
