from django.urls import path

from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('estudiante',views.EstudianteView.as_view(),name='estudiante'),
    path('estudiante/<str:id_estudiante>',views.EstudianteDetailView.as_view(),name='estudiante_detail'),
    path('curso',views.CursoView.as_view(),name='curso'),
    path('nota',views.NotaView.as_view(),name='nota'),
    path('nota/<str:id_estudiante>',views.NotasAlumView.as_view(),name='nota_estudiante'),
    path('nota/<str:id_estudiante>/<str:id_nota>',views.NotaDetailView.as_view(),name='nota_detail'),
    path('promedio',views.PromedioView.as_view(),name='promedio'),
]
