from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
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
    url(r'^getturn/', views.getCurrentTurn, name = 'getCurrentTurn'),
    url(r'^new/', views.UserFormView.as_view(), name='createNewUser'),
    url(r'^login/$', views.loginView, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]