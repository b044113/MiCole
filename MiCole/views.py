from django.shortcuts import render
from django.urls import reverse
from django.views import generic
#from analisis.models import Symbol, Market, SymbolValue

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    #num_symbols = Symbol.objects.all().count()
    #num_markets = Market.objects.all().count()
    #num_instances = SymbolValue.objects.all().count()
    # Libros disponibles (status = 'a')
    #num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    #num_authors = Author.objects.count()  # El 'all()' esta implícito por defecto.

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={},
    )