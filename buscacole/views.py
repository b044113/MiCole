from django.shortcuts import render

import operator, functools
from escuelas.views import SchoolListView
from django.db.models import Q
from django.http import HttpResponse
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
        grade_id = request.GET['grade']

        query_list = q.split()
        schools = School.objects.filter(functools.reduce(operator.and_,
                                            (Q(locality__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(city__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(province__name__icontains=q) for q in query_list))
                                        )
        schools = schools.filter(Q(vacancy__grade__id = grade_id) & Q(vacancy__vacancies__gt = 0)).distinct

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

