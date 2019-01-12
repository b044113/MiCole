from django.shortcuts import render

import operator, functools
from escuelas.views import SchoolListView
from django.db.models import Q
from django.http import HttpResponse
from escuelas.models import School

from django.shortcuts import render

def search_form(request):
    return render(request, 'buscacole/formulario_busqueda.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        schools = School.objects.filter(locality__name__icontains=q)
        return render(request, 'escuelas/school_list.html',
                      {'school_list': schools, 'query': q})
    else:
        return HttpResponse('Especifique un criterio de búsqueda.')


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
