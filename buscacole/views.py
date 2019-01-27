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
        and 'grade_1' in request.GET and request.GET['grade_1']:

        q = request.GET['q']
        query_list = q.split()

        #Filtrar por ubicación
        schools = School.objects.filter(functools.reduce(operator.and_,
                                            (Q(locality__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(city__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(province__name__icontains=q) for q in query_list))
                                        )

        #Filtrar por grados
        grades = {}
        for k in request.GET:
            if k != 'q':
                if request.GET[k]:
                    if request.GET[k] in grades:
                        grades[request.GET[k]] += 1
                    else:
                        grades[request.GET[k]] = 1


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


