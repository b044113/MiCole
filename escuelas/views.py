from django.views import generic
from .models import School

# Create your views here.
class SchoolListView(generic.ListView):
    model = School

    def get_queryset(self):
        return School.objects.filter(name__icontains='a')[:5]  # Get 5 books containing the title war

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SchoolListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class SchoolDetailView(generic.DetailView):
    model = School