# articles/forms.py
from django import forms

from .models import Article, Location


class ArticleForm(forms.ModelForm):
    # Extra field for creating a new location
    new_location = forms.CharField(
        required=False,
        label="New Location",
        help_text="Enter a new location if it's not in the dropdown.",
    )

    class Meta:
        model = Article
        fields = ["title", "people", "location", "content"]  # only model fields

    def save(self, commit=True):
        # If user entered a new location, create or get it
        new_location_name = self.cleaned_data.get("new_location")
        if new_location_name:
            location, _ = Location.objects.get_or_create(name=new_location_name)
            self.instance.location = location
        return super().save(commit=commit)
