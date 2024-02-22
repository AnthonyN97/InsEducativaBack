from django.urls import path

from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('estudiante',views.EstudianteView.as_view(),name='estudiante'),
]
