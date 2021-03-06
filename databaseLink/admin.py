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
