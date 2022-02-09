from django.urls import path
from django.views.generic.detail import DetailView
from . import views




app_name = 'home_page'

urlpatterns = [
    path('', views.Index.as_view(), name = 'index')
]