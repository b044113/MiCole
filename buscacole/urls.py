from django.conf.urls import url

from . import views

app_name = 'buscacole'

urlpatterns = [

    url(r'^$', views.search_form, name='searchform'),
    url(r'^formulario_busqueda/$', views.search, name="search"),

    url(r'^ajax/load-grades/', views.load_grades, name='ajax_load_grades'),  # <-- this one here

]

