from django.shortcuts import render


def home(request, **kwargs):
    template_name = "home/home.html"
    context = dict()
    return render(request, template_name, context)


def privacidad(request, **kwargs):
    template_name = "home/privacidad.html"
    context = dict()
    return render(request, template_name, context)
