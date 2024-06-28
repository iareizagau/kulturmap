import requests
import pandas as pd
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import JsonResponse


from apps.culture.models import Events, EVENT_TYPE

from KulturMap import settings

def play_console(request, **kwargs):
    json_data = [
            {
                "relation": [
                "delegate_permission/common.handle_all_urls"
                ],
                "target": {
                "namespace": "android_app",
                "package_name": "app.run.a.opendataeuskadi_z6zzxsqmma_ew.twa",
                "sha256_cert_fingerprints": [
                    "94:BE:68:73:23:3D:22:94:5E:07:9B:3B:7A:E5:ED:B2:43:62:86:89:02:BB:BC:A7:FB:97:EE:DA:FE:AD:67:6A"
                ]
                }
            }
            ]

    return JsonResponse(json_data)
    

# Create your views here.
def culture(request, **kwargs):
    template_name = "culture/home.html"
    context = dict()
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)
    events = Events.objects.filter(startDate__gte=start_date, startDate__lte=end_date).order_by('startDate')
    # events = Events.objects.all()
    total_municipalityEu = Events.objects.values_list('municipalityEu', flat=True).order_by('municipalityEu').distinct()
    total_language = set(Events.objects.values_list('language', flat=True).order_by('language').distinct())
    total_typeEu = Events.objects.values_list('typeEu', flat=True).order_by('typeEu').distinct()
    context['distance'] = 20

    if request.POST:
        add_event = request.POST.get('addEvent')
        type = EVENT_TYPE.get(request.POST.get('type'))
        if add_event:
            Events.objects.create(
                events_id='',
                type=type,
                typeEs='',
                typeEu=request.POST.get('type'),
                nameEs=request.POST.get('name'),
                nameEu=request.POST.get('name'),
                startDate=datetime.strptime(request.POST.get('startDate2'), '%Y-%m-%dT%H:%M'),
                endDate='',
                publicationDate='',
                language='',
                sourceNameEs='',
                sourceNameEu='',
                sourceUrlEs='',
                sourceUrlEu='',
                descriptionEs=request.POST.get('description'),
                descriptionEu=request.POST.get('description'),
                municipalityEs='',
                municipalityEu='',
                municipalityLatitude='',
                municipalityLongitude='',
                municipalityNoraCode='',
                provinceNoraCode='',
                establishmentEs=request.POST.get('establishment'),
                establishmentEu=request.POST.get('establishment'),
                urlEventEs='',
                urlEventEu='',
                urlNameEs='',
                urlNameEu='',
                openingHoursEs='',
                openingHoursEu='',
                priceEs=request.POST.get('price'),
                priceEu=request.POST.get('price'),
                purchaseUrlEs='',
                purchaseUrlEu='',
                images='',
                attachment='',
                companyEs='',
                companyEu='',
                placeEs='',
                placeEu='',
                online='',
                urlOnlineEs='',
                urlOnlineEu='',
            )
            pass
        else:
            events = Events.objects.filter(startDate__gte=start_date).order_by('startDate')
            ver_mas = request.POST.get('ver_mas')
            language = request.POST.get('language')
            municipalityEu = request.POST.get('municipalityEu')
            typeEu = request.POST.get('typeEu')
            provinceNoraCode = request.POST.get('provinceNoraCode')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            name = request.POST.get('name')

            # Apply filters based on form data
            if name:
                events = events.filter(nameEu__icontains=name)
            if language:
                events = events.filter(language=language)
            if municipalityEu:
                events = events.filter(municipalityEu=municipalityEu)
            if typeEu:
                events = events.filter(typeEu=typeEu)
            if provinceNoraCode:
                events = events.filter(provinceNoraCode=provinceNoraCode)
            if startDate:
                start_date = datetime.strptime(startDate, "%Y-%m-%d").date()
                events = events.filter(startDate=start_date)
            if startDate and endDate:
                start_date = datetime.strptime(startDate, "%Y-%m-%d")
                end_date = datetime.strptime(endDate, "%Y-%m-%d")
                events = events.filter(startDate__gte=start_date, startDate__lte=end_date)
            if ver_mas:
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=60)
                events = events.filter(startDate__gte=start_date, startDate__lte=end_date)

    context['objects'] = events
    context['municipalities'] = total_municipalityEu
    context['total_language'] = total_language
    context['total_typeEu'] = total_typeEu
    context['start_date'] = start_date
    context['end_date'] = end_date
    return render(request, template_name, context)


def event(request, **kwargs):
    template_name = 'culture/event.html'
    obj = Events.objects.get(id=kwargs['pk'])
    context = dict()
    context['obj'] = obj
    return render(request, template_name, context)


from django.views.generic import ListView
from django.utils import timezone


class HomeView(ListView):
    model = Events
    template_name = "culture/home2.html"
    context_object_name = "objects"
    paginate_by = 3*100
    ordering = "startDate"

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "culture/card.html"
        else:
            return self.template_name


    def get_queryset(self):
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)
        qs = Events.objects.filter(startDate__gte=start_date).order_by('startDate')
        return qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context['distance'] = 10
        return context


