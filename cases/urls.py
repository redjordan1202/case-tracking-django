from django.urls import path
from django.views.generic.detail import DetailView
from . import views




app_name = 'cases'

urlpatterns = [
    path('', views.IndexView, name='cases'),
    path('<str:pk>/details/', views.DetailsView.as_view(), name='details'),
    path('process/', views.ProcessView, name='process'),
    path('generate/', views.GenerateView, name='generate' ),
    path('unsent/', views.UnsentView, name='unsent'),
    path('<str:pk>/update/',views.UpdateView, name='update')
]