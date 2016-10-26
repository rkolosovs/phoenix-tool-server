from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^armydata/', views.armyData, name = 'armyData'),
    url(r'^buildingdata/', views.buildingData, name = 'buildingData'),
]