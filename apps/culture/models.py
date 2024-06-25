from django.db import models
from datetime import datetime


# Create your models here.
class Events(models.Model):
    events_id = models.CharField(max_length=1000)
    type = models.IntegerField()
    typeEs = models.CharField(max_length=1000)
    typeEu = models.CharField(max_length=1000)
    nameEs = models.TextField()
    nameEu = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()
    publicationDate = models.DateField()
    language = models.CharField(max_length=10)
    sourceNameEs = models.CharField(max_length=1000)
    sourceNameEu = models.CharField(max_length=1000)
    sourceUrlEs = models.TextField()
    sourceUrlEu = models.TextField()
    descriptionEs = models.TextField()
    descriptionEu = models.TextField()
    municipalityEs = models.CharField(max_length=108)
    municipalityEu = models.CharField(max_length=108)
    municipalityLatitude = models.FloatField()
    municipalityLongitude = models.FloatField()
    municipalityNoraCode = models.CharField(max_length=107)
    provinceNoraCode = models.CharField(max_length=106)
    establishmentEs = models.CharField(max_length=105)
    establishmentEu = models.CharField(max_length=105)
    urlEventEs = models.CharField(max_length=255)
    urlEventEu = models.CharField(max_length=255)
    urlNameEs = models.CharField(max_length=103)
    urlNameEu = models.CharField(max_length=103)
    openingHoursEs = models.CharField(max_length=350, null=True)
    openingHoursEu = models.CharField(max_length=350, null=True)
    priceEs = models.CharField(max_length=101, null=True)
    priceEu = models.CharField(max_length=101, null=True)
    purchaseUrlEs = models.CharField(max_length=1000, null=True)
    purchaseUrlEu = models.CharField(max_length=1000, null=True)
    images = models.CharField(max_length=1000, null=True)
    attachment = models.TextField(max_length=1100, null=True)
    companyEs = models.CharField(max_length=1100, null=True)
    companyEu = models.CharField(max_length=1100, null=True)
    placeEs = models.CharField(max_length=1100, null=True)
    placeEu = models.CharField(max_length=1100, null=True)
    online = models.CharField(max_length=1100, null=True)
    urlOnlineEs = models.CharField(max_length=1100, null=True)
    urlOnlineEu = models.CharField(max_length=1100, null=True)
    created = models.DateField(auto_created=True, null=True)
    updated = models.DateField(auto_created=True, auto_now_add=True, null=True)


EVENT_TYPE = {
    'Antzerkia': 14
}
