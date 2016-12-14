from django.contrib import admin
from .models import Realm, RealmMembership, Character, Building, Field, RealmTerritory, River, TurnOrder, Troop, \
    TurnEvent, BuildEvent, MoveEvent, RecruitmentEvent, BattleEvent, CommentEvent, TreasuryEvent

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
admin.site.register(MoveEvent)
admin.site.register(RecruitmentEvent)
admin.site.register(BattleEvent)
admin.site.register(CommentEvent)
admin.site.register(TreasuryEvent)
