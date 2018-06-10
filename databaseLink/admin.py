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

from django.contrib import admin
from .models import Realm, RealmMembership, Character, Building, Field, RealmTerritory, River, TurnOrder, Troop, \
    TurnEvent, BuildEvent, ShootEvent, MoveEvent, RecruitmentEvent, BattleEvent, CommentEvent, TreasuryEvent, \
    LastSavedTimeStamp, MergeEvent, TransferEvent, SplitEvent, MountEvent

admin.site.register(Realm)
admin.site.register(RealmMembership)
admin.site.register(Character)
admin.site.register(Building)
admin.site.register(Field)
admin.site.register(River)
admin.site.register(TurnOrder)
admin.site.register(Troop)
admin.site.register(RealmTerritory)
admin.site.register(TurnEvent)
admin.site.register(BuildEvent)
admin.site.register(ShootEvent)
admin.site.register(MoveEvent)
admin.site.register(MergeEvent)
admin.site.register(TransferEvent)
admin.site.register(SplitEvent)
admin.site.register(RecruitmentEvent)
admin.site.register(BattleEvent)
admin.site.register(CommentEvent)
admin.site.register(TreasuryEvent)
admin.site.register(LastSavedTimeStamp)
admin.site.register(MountEvent)
