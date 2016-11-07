from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^savearmydata/', views.saveArmyData, name = 'saveArmyData'),
    url(r'^armydata/', views.armyData, name = 'armyData'),
    url(r'^savebuildingdata/', views.saveBuildingData, name = 'saveBuildingData'),
    url(r'^buildingdata/', views.buildingData, name = 'buildingData'),
    url(r'^savefielddata/', views.saveFieldData, name = 'saveFieldData'),
    url(r'^fielddata/', views.fieldData, name = 'fieldData'),
    url(r'^gettoken/', views.getCSRFToken, name = 'getCSRFToken'),
    url(r'^saveriverdata/', views.saveRiverData, name = 'saveRiverData'),
    url(r'^getriverdata/', views.getRiverData, name = 'getRiverData'),
    url(r'^saveborderdata/', views.saveBorderData, name = 'saveBorderData'),
    url(r'^getborderdata/', views.getBorderData, name = 'getBorderData'),
    url(r'^testclient/', views.defaultPage, name = 'defaultPage')

]