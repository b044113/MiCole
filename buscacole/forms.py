from django import forms


class SearchForm(forms.Form):
    search_criteria = forms.TextInput(help_text="Ingrese la zona deseada")
