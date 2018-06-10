# Copyright 2018 Janos Klieber, Roberts Kolosovs, Peter Spieler
# This file is part of Phoenixserver.
#
# Phoenixserver is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Phoenixserver is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Phoenixserver.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^savearmydata/', views.saveArmyData, name='saveArmyData'),
    url(r'^armydata/', views.armyData, name='armyData'),
    url(r'^savebuildingdata/', views.saveBuildingData, name='saveBuildingData'),
    url(r'^buildingdata/', views.buildingData, name='buildingData'),
    url(r'^savefielddata/', views.saveFieldData, name='saveFieldData'),
    url(r'^fielddata/', views.fieldData, name='fieldData'),
    url(r'^gettoken/', views.getCSRFToken, name='getCSRFToken'),
    url(r'^getlastsavedtimestamp/', views.getLastSavedTimeStamp, name='getLastSavedTimeStamp'),
    url(r'^saveriverdata/', views.saveRiverData, name='saveRiverData'),
    url(r'^getriverdata/', views.getRiverData, name='getRiverData'),
    url(r'^saveborderdata/', views.saveBorderData, name='saveBorderData'),
    url(r'^getborderdata/', views.getBorderData, name='getBorderData'),
    url(r'^getturn/', views.getCurrentTurn, name='getCurrentTurn'),
    url(r'^nextturn/', views.postNextTurn, name='postNextTurn'),
    url(r'^moveevent/', views.postMoveEvent, name='postMoveEvent'),
    url(r'^battleevent/', views.postBattleEvent, name='postBattleEvent'),
    url(r'^shootevent/', views.postShootEvent, name='postShootEvent'),
    url(r'^mergeevent/', views.postMergeEvent, name='postMergeEvent'),
    url(r'^transferevent/', views.postTransferEvent, name='postTransferEvent'),
    url(r'^splitevent/', views.postSplitEvent, name='postSplitEvent'),
    url(r'^mountevent/', views.postMountEvent, name='postMountEvent'),
    url(r'^checkevent/', views.checkEvent, name='checkEvent'),
    url(r'^deleteevent/', views.deleteEvent, name='deleteEvent'),
    url(r'^getevents/', views.getPendingEvents, name='getPendingEvents'),
    url(r'^getrealms/', views.getRealms, name='getRealms'),
    url(r'^new/', views.UserFormView.as_view(), name='createNewUser'),
    url(r'^login/$', views.loginView, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]