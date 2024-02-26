from django.urls import path

from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('estudiante',views.EstudianteView.as_view(),name='estudiante'),
    path('curso',views.CursoView.as_view(),name='curso'),
    path('nota',views.NotaView.as_view(),name='nota'),
    path('promedio',views.PromedioView.as_view(),name='promedio'),
]
