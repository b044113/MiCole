from django import forms
from escuelas.models import School, Grade, Level


#Iterator for levels to pass to the dropdown field
class LevelListIterable(object):
    def __iter__(self):
        levelList = Level.objects.all().only('id', 'name').order_by('id')
        levelChoices = levelList.values_list('id', 'name').distinct()
        return levelChoices.__iter__()

class SearchForm(forms.Form):

    #Location Search Crieria Text Input
    searchText = forms.CharField(label='Criterio de Búsqueda', max_length=100)
    searchText.widget = forms.TextInput(attrs={'name': 'q', 'class':'form-control'})

    #Level & Grade Search Criteria
    levels = LevelListIterable()
    levelDropDown = forms.CharField(label='Nivel')
    levelDropDown.widget = forms.Select(choices=levels, attrs={'id': 'level',
                                                               'name': 'level',
                                                               'class':'form-control'})

    #levels = LevelListIterable()
    gradeDropDown = forms.CharField(label='Grado')
    gradeDropDown.widget = forms.Select(attrs={'id': 'grade',
                                                'name': 'grade',
                                                'class': 'form-control'})



