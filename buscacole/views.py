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
    if 'q' in request.GET and request.GET['q'] \
            and 'level' in request.GET and request.GET['level']:
        q = request.GET['q']
        level_id = request.GET['level']

        query_list = q.split()
        schools = School.objects.filter(functools.reduce(operator.and_,
                                            (Q(locality__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(city__name__icontains=q) for q in query_list)) |
                                        functools.reduce(operator.and_,
                                            (Q(province__name__icontains=q) for q in query_list))
                                        )
        schools = schools.filter(Q(vacancy__grade__level = level_id) & Q(vacancy__vacancies__gt = 0))

        return render(request, 'escuelas/school_list.html',
                      {'school_list': schools, 'query': q})
    else:
        return HttpResponse('Especifique un criterio de búsqueda.')


def load_grades(request):
    if 'level' in request.GET and request.GET['level']:
        level_id = request.GET['level']
        grades = Grade.objects.filter(level_id=level_id).order_by('name')
        return render(request, 'hr/grade_dropdown_list_options.html', {'grades': grades})
    else:
        return HttpResponse('Seleccione un nivel de educación.')



class SchoolSearchListView(SchoolListView):
    """
    Display a School List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(SchoolSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                functools.reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                functools.reduce(operator.and_,
                       (Q(content__icontains=q) for q in query_list))
            )

        return result
# Create your views here.
