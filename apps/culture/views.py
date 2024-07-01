import requests
import pandas as pd
from datetime import datetime, timedelta
from geopy.distance import geodesic

from django.shortcuts import render
from django.http import JsonResponse


from apps.culture.models import Events, EVENT_TYPE

from KulturMap import settings

def play_console(request, **kwargs):
    json_data = [{
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "eus.maps.kultur.twa",
        "sha256_cert_fingerprints": ["2E:3D:04:FC:10:C2:2C:33:6D:47:8C:75:F3:12:A0:4A:CC:2F:25:50:0E:EB:6D:B6:7B:E9:30:30:E1:8C:3F:45"]
      }
    }]

    return JsonResponse(json_data, safe=False)
    

# Create your views here.
def culture(request, **kwargs):
    template_name = "culture/home.html"
    context = dict()
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)
    events = Events.objects.filter(startDate__gte=start_date, startDate__lte=end_date).order_by('startDate')
    # events = Events.objects.all()
    total_municipalityEu = Events.objects.values_list('municipalityEu', flat=True).order_by('municipalityEu').distinct()
    total_typeEu = ['Kontzertua', 'Antzerkia', 'Bertsolaritza', 'Dantza', 'Jaiak', 'Jaialdia', 'Formakuntza', 'Ekitaldiak/jardunaldiak', 'Erakusketa', 'Haur jarduera', 'Hitzaldia', 'Lehiaketa', 'Zinema eta ikus-entzunezkoak', 'Azoka', 'Bestelakoa',]
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
            custom_distance = request.POST.get('custom_distance')
            typeEu = request.POST.get('typeEu')
            provinceNoraCode = request.POST.get('provinceNoraCode')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            name = request.POST.get('name')
            if request.session.get('filters'):
                if typeEu in request.session['filters']:
                    request.session['filters'].remove(typeEu)
                else:
                    request.session['filters'].append(typeEu)
                request.session['filters'] = request.session['filters']
            else:
                request.session['filters'] = [typeEu]
            context['filters'] = request.session['filters']
            print("context['filters']", context['filters'])
            if name:
                events = events.filter(nameEu__icontains=name)
            if language:
                events = events.filter(language=language)
            if municipalityEu:
                events = events.filter(municipalityEu=municipalityEu)
                city = Events.objects.filter(municipalityEu=municipalityEu).first()
                context['city'] = city
                context['custom_distance'] = int(float(custom_distance) * 1000)
                lat_city = city.municipalityLatitude
                lng_city = city.municipalityLongitude
                city_coords = (lat_city, lng_city)
                start_date = datetime.strptime(startDate, "%Y-%m-%d")
                end_date = datetime.strptime(endDate, "%Y-%m-%d")
                event_list = Events.objects.filter(startDate__gte=start_date, startDate__lte=end_date).order_by('startDate')
                events = []
                for index, event in enumerate(event_list):
                    lat_event = event.municipalityLatitude
                    lng_event = event.municipalityLongitude                    
                    event_coords = (lat_event, lng_event)
    
                    distance = geodesic(city_coords, event_coords).kilometers
                    if distance <= float(custom_distance):
                        events.append(event)
                        print(f"Distance from city to event {event.id}: {distance:.2f} km")                    

            if typeEu:
                if request.session['filters']:
                    events = events.filter(typeEu__in=request.session['filters'])
                else:
                    events = Events.objects.filter(startDate__gte=start_date).order_by('startDate')
            if provinceNoraCode:
                events = events.filter(provinceNoraCode=provinceNoraCode)           
            if ver_mas:
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=60)
                events = events.filter(startDate__gte=start_date, startDate__lte=end_date)

    context['objects'] = events
    context['municipalities'] = total_municipalityEu
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
    paginate_by = 3*20
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


