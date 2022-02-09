from django.shortcuts import render
from django.views import generic
from django.views.generic.base import TemplateView
# Create your views here.

class Index(TemplateView):
    template_name = 'home_page/index.html'