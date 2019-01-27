from django.shortcuts import render

import operator, functools
from escuelas.views import SchoolListView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from escuelas.models import School, Grade, Level

from django.shortcuts import render

def search_form(request):
    levels = Level.objects.all()
    return render(request, 'buscacole/formulario_busqueda.html', {'levels': levels})


def search(request):
    """

    :param request:
    :return: Realiza la búsqueda de los colegios a partir de la zona y el nivel/grado

    """
    if 'q' in request.GET and request.GET['q'] \
            and 'grade' in request.GET and request.GET['grade']:
        q = request.GET['q']
        grades = {request.GET['grade']: 1}

        if 'grade_2' in request.GET and request.GET['grade_2']:
            if request.GET['grade_2'] in grades:
                grades[request.GET['grade_2']] += 1
            else:
                grades[request.GET['grade_2']] = 1

        if 'grade_3' in request.GET and request.GET['grade_3']:
            if request.GET['grade_3'] in grades:
                grades[request.GET['grade_3']] += 1
            else:
                grades[request.GET['grade_3']] = 1

        if 'grade_4' in request.GET and request.GET['grade_4']:
            if request.GET['grade_4'] in grades:
                grades[request.GET['grade_4']] += 1
            else:
                grades[request.GET['grade_4']] = 1

        if 'grade_5' in request.GET and request.GET['grade_5']:
            if request.GET['grade_5'] in grades:
                grades[request.GET['grade_5']] += 1
            else:
                grades[request.GET['grade_5']] = 1

        query_list = q.split()
        schools = School.objects.filter(functools.reduce(operator.and_,
                                            (Q(locality__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(city__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(province__name__icontains=q) for q in query_list))
                                        )

        for k, v in grades.items():
            print(k,v)
            schools = schools.filter(Q(vacancy__grade__id = k) & Q(vacancy__vacancies__gte = v))

        schools = schools.filter().distinct
        return render(request, 'escuelas/school_list.html',
                      {'school_list': schools, 'query': q})
    else:
        return HttpResponse('Especifique un criterio de búsqueda.')


def load_grades(request):
    """

    :param request:
    :return: Rellena los valores de los grados a partir del nivel seleccionado
    utilizando el archivo grade_dropdown_list_option.html

    """
    if 'level' in request.GET and request.GET['level']:
        level_id = request.GET['level']
        grades = Grade.objects.filter(level__id=level_id).order_by('name')
        return render(request, 'buscacole/grade_dropdown_list_options.html', {'grades': grades})
    else:
        return HttpResponse('Seleccione un nivel de educación.')


from buscacole.forms import SearchForm

def search_form2(request):
    form = SearchForm()

    return render(request, 'buscacole/formulario_busqueda2.html', {'form': form})

def search2(request):
    """

    :param request:
    :return: Realiza la búsqueda de los colegios a partir de la zona y el nivel/grado

    """
    if 'searchText' in request.GET and request.GET['searchText'] \
            and 'gradeDropDown' in request.GET and request.GET['gradeDropDown']:
        grade_id = request.GET['gradeDropDown']
        q = request.GET['searchText']

        query_list = q.split()
        schools = School.objects.filter(functools.reduce(operator.and_,
                                            (Q(locality__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(city__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(province__name__icontains=q) for q in query_list))
                                        )
        schools = schools.filter(Q(vacancy__grade__id=grade_id) & Q(vacancy__vacancies__gt=0)).distinct

        return render(request, 'escuelas/school_list.html',
                      {'school_list': schools, 'query': q})
    else:
        return HttpResponse('Especifique un criterio de búsqueda.')
