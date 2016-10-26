from django.http import HttpResponse
from django.template import loader
from django.core import serializers
import json
from .models import Truppen
from .models import Ruestgueter

def armyData(request):
    all_troops_data = serializers.serialize('python', Truppen.objects.all())
    data = [d['fields'] for d in all_troops_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)

def buildingData(request):
    all_buildings_data = serializers.serialize('python', Ruestgueter.objects.all())
    data = [d['fields'] for d in all_buildings_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)