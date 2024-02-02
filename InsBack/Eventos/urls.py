from django.urls import path

from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('eventos',views.EventosView.as_view(),name='eventos'),
    path('evento/<int:evento_id>',views.EventoDetailView.as_view())
]
