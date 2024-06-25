from django.contrib import admin
from .models import Events


# Register your models here.
@admin.register(Events)
class Events(admin.ModelAdmin):
    list_display = ('id', 'events_id', 'nameEu', 'startDate', 'endDate', 'type', 'typeEu', 'typeEs', 'online',
                    'urlOnlineEu', 'purchaseUrlEu', 'urlNameEu', 'urlEventEu', 'sourceUrlEu',
                    'sourceNameEs', 'municipalityEu', 'openingHoursEu', 'priceEu', 'placeEu', 'companyEu',)
    list_filter = ('type', 'typeEu', )
    search_fields = ('nameEu', )
