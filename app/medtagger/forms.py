from django import forms
# from django.contrib.auth.models import User
from medtagger.models import Tag, Author
from dal import autocomplete


class TagForm(forms.Form):
    wikiLabel = autocomplete.Select2ListChoiceField(
        widget=autocomplete.ListSelect2(url='tag-autocomplete'),
        label="Search Wikidata Entry"
    )
