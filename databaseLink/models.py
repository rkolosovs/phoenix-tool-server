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

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Realm(models.Model):
    tag = models.CharField(max_length=3)
    name = models.CharField(max_length=250)
    color = models.CharField(max_length=11, default='000,000,000')
    homeTurf = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def short(self):
        return str(self.tag)

    def __str__(self):
        if self.active:
            return self.name + ' (' + str(self.tag) + ')'
        else:  # mark realms lost to history with X Realm (rlm) X
            return 'X ' + self.name + ' (' + str(self.tag) + ') X'


class RealmMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ', ' + str(self.realm)


class Character(models.Model):
    charName = models.CharField(max_length=250)
    x = models.IntegerField()
    y = models.IntegerField()
    firstName = models.CharField(max_length=250, null=True, blank=True)
    secondName = models.CharField(max_length=250, null=True, blank=True)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.charName


class Building(models.Model):
    DIRECTIONS = (
        ("nw", "north-west"),
        ("ne", "north-east"),
        ("e", "east"),
        ("se", "south-east"),
        ("sw", "south-west"),
        ("w", "west"),
    )
    type_names = ["castle", "city", "fortress", "capital", "capitalFort", "wall", "harbor", "bridge", "street"]
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, default="")
    type = models.IntegerField()
    direction = models.CharField(max_length=2, null=True, blank=True, choices=DIRECTIONS)
    firstX = models.IntegerField(null=True, blank=True)
    firstY = models.IntegerField(null=True, blank=True)
    secondX = models.IntegerField(null=True, blank=True)
    secondY = models.IntegerField(null=True, blank=True)
    guardCount = models.IntegerField(null=True, blank=True)
    buildPoints = models.IntegerField(null=True, blank=True)

    def __str__(self):
        result = Realm.short(self.realm) + ' ' + str(self.type_names[self.type]) + ' ' + str(self.name)
        if 0 <= self.type <= 5:
            result += ' (' + str(self.firstX) + ', ' + str(self.firstY) + ') ' + str(self.buildPoints) + ' BP'
        if 5 == self.type:
            result += ' facing ' + str(self.direction) + ', ' + str(self.guardCount) + ' guards'
        if 6 <= self.type <= 8:
            result += ' between (' + str(self.firstX) + ', ' + str(self.firstY) + ') and (' + str(self.secondX) + \
               ', ' + str(self.secondY) + ')'
        return result


class Field(models.Model):
    type = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        if self.type == 0:
            type_str = 'shallows'
        elif self.type == 1:
            type_str = 'deepsea'
        elif self.type == 2:
            type_str = 'lowlands'
        elif self.type == 3:
            type_str = 'woods'
        elif self.type == 4:
            type_str = 'hills'
        elif self.type == 5:
            type_str = 'highlands'
        elif self.type == 6:
            type_str = 'mountains'
        elif self.type == 7:
            type_str = 'desert'
        elif self.type == 8:
            type_str = 'swamp'
        else:
            type_str = 'undefined'
        return '(' + str(self.x) + ', ' + str(self.y) + ') ' + type_str


class RealmTerritory(models.Model):
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return Realm.short(self.realm) + ', (' + str(self.x) + ', ' + str(self.y) + ')'


class River(models.Model):
    firstX = models.IntegerField()
    firstY = models.IntegerField()
    secondX = models.IntegerField()
    secondY = models.IntegerField()

    def __str__(self):
        return 'river between (' + str(self.firstX) + ', ' + str(self.firstY) + ') and (' + str(self.secondX) \
               + ', ' + str(self.secondY) + ')'


class Troop(models.Model):
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, null=True)
    armyId = models.IntegerField()
    count = models.IntegerField()
    leaders = models.IntegerField()
    mounts = models.IntegerField()
    lkp = models.IntegerField()
    skp = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    movementPoints = models.IntegerField()
    heightPoints = models.IntegerField()
    isGuard = models.BooleanField(default=False)
    isLoadedIn = models.IntegerField(default=None, blank=True, null=True)
    STATUS_CHOICES = (("tobe", "tobe"), ("active", "active"), ("inactive", "inactive"))
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default="active",
    )

    def short(self):
        return Realm.short(self.realm) + ' ' + str(self.armyId)

    def __str__(self):
        is_guard = ''
        status = ''
        if str(self.status) == "tobe":
            status = '(to be) '
        elif str(self.status) == "inactive":
            status = '(inactive) '
        if self.isGuard:
            is_guard = ', Guard'
        return status + Realm.short(self.realm) + ', ' + str(self.armyId) + ', (' + str(self.x) + ', ' + str(self.y) \
            + ')' + ', Count: ' + str(self.count) + ', Leaders: ' + str(self.leaders) + is_guard + ', MP: ' \
            + str(self.movementPoints) + ', HP: ' + str(self.heightPoints)


class TurnOrder(models.Model):
    # e.g. (148, 3, usa) means: in turn 148 usa is 3rd in the turn order
    turnNumber = models.IntegerField()
    turnOrder = models.IntegerField()
    realm = models.ForeignKey(Realm, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.realm is None:
            return str(self.turnNumber) + ', ' + str(self.turnOrder) + ', None'
        else:
            return str(self.turnNumber) + ', ' + str(self.turnOrder) + ', ' + Realm.short(self.realm)


class Event(models.Model):
    prerequisiteEvents = models.ManyToManyField('self', null=True)
    turn = models.ForeignKey(TurnOrder, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class MoveEvent(Event):
    # Used to record movement of armies
    troop = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL)
    from_x = models.IntegerField()
    from_y = models.IntegerField()
    to_x = models.IntegerField()
    to_y = models.IntegerField()

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.troop is None:
            troop_str = '*no army*'
        else:
            troop_str = Realm.short(self.troop.realm) + ', ' + str(self.troop.armyId)
        return troop_str + ' from (' + str(self.from_x) + ', ' + str(self.from_y) + '), ' + \
            'to (' + str(self.to_x) + ', ' + str(self.to_y) + '), ' + processed_str + ', ' + str(self.date)


class BattleEvent(Event):
    # Used to record battles and their outcome
    participants = models.ManyToManyField(Troop)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        participants_str = '['
        for p in self.participants.all():
            participants_str += '('+Realm.short(p.realm)+','+str(p.armyId)+')'
        participants_str += ']'
        return participants_str + ', (' + str(self.x) + ', ' + str(self.y) + '), ' + processed_str + ', ' + \
            str(self.date)


class BuildEvent(Event):
    # Used to record builds commissioned
    # TODO: different building types need different fields
    x = models.IntegerField()
    y = models.IntegerField()
    type = models.IntegerField()

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        return '(' + str(self.x) + ', ' + str(self.y) + '), ' + str(self.type) + ', ' + processed_str + \
               ', ' + str(self.date)


class ShootEvent(Event):
    # Used to record all the shooting
    shooter = models.ForeignKey(Troop, on_delete=models.CASCADE, null=True)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    from_x = models.IntegerField()
    from_y = models.IntegerField()
    to_x = models.IntegerField()
    to_y = models.IntegerField()
    target = models.CharField(max_length=10, null=True, blank=True)
    lkp_count = models.IntegerField()
    skp_count = models.IntegerField()

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.shooter is None:
            shooter_str = '*no army*'
        else:
            shooter_str = Realm.short(self.shooter.realm) + ', ' + str(self.shooter.armyId)

        return shooter_str + ', ' + str(self.from_x) + ', ' + str(self.from_y) + '(' + str(self.to_x) + ', ' + str(self.to_y) + '), ' \
               + str(self.target)+ ', '+ str(self.lkp_count) + ', ' + str(self.skp_count) \
               + ', ' + processed_str + ', ' + str(self.date)


class RecruitmentEvent(Event):
    # Used to record recruitment started
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    army = models.ForeignKey(Troop, on_delete=models.CASCADE, null=True)
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)
    footmen = models.IntegerField()
    horsemen = models.IntegerField()
    leaders = models.IntegerField()
    lkp = models.IntegerField()
    skp = models.IntegerField()
    ships = models.IntegerField()
    lks = models.IntegerField()
    sks = models.IntegerField()

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        output = str(self.building) + ' recruits '
        if not self.footmen.null:
            output += str(self.footmen) + ' footmen, '
        if not self.horsemen.null:
            output += str(self.horsemen) + ' horsemen, '
        if not self.leaders.null:
            output += str(self.leaders) + ' leaders, '
        if not self.lkp.null:
            output += str(self.lkp) + ' light catapults, '
        if not self.skp.null:
            output += str(self.skp) + ' heavy catapults, '
        if not self.ships.null:
            output += str(self.ships) + ' ships, '
        if not self.lks.null:
            output += str(self.lks) + ' light warships, '
        if not self.sks.null:
            output += str(self.sks) + ' heavy warships, '
        output += processed_str + ', ' + str(self.date)
        return output


class TreasuryEvent(Event):
    # Used to record changes in treasury
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    change = models.IntegerField()

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.change.to_python() >= 0:
            direction = ' gains '
        else:
            direction = ' loses '
        return Realm.short(self.realm) + direction + str(abs(self.change.to_python())) + ', ' + processed_str + \
            ', ' + str(self.date)


class MergeEvent(Event):
    # Used to record the Merging of armies
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    fromArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL, related_name='+')
    toArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL, related_name='+')
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.fromArmy is None:
            troop_str_from = '*no army*'
        else:
            troop_str_from = Realm.short(self.fromArmy.realm) + ', ' + str(self.fromArmy.armyId)
        if self.toArmy is None:
            troop_str_to = '*no army*'
        else:
            troop_str_to = Realm.short(self.toArmy.realm) + ', ' + str(self.toArmy.armyId)

        return troop_str_from + ', merges into ' + troop_str_to + ' on Field (' + str(self.x) +\
            ',' + str(self.y) + ').' + processed_str + ', ' + str(self.date)


class TransferEvent(Event):
    # Used to record the transfer of troops from one army to another
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    fromArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL, related_name='+')
    armyFromType = models.IntegerField()
    toArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL, related_name='+')
    armyToType = models.IntegerField()
    troops = models.IntegerField()
    leaders = models.IntegerField()
    mounts = models.IntegerField()
    lkp = models.IntegerField()
    skp = models.IntegerField()
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.fromArmy is None:
            troop_str_from = '*no army*'
        else:
            troop_str_from = Realm.short(self.fromArmy.realm) + ', ' + str(self.fromArmy.armyId)
        if self.toArmy is None:
            troop_str_to = '*no army*'
        else:
            troop_str_to = Realm.short(self.toArmy.realm) + ', ' + str(self.toArmy.armyId)
        result = troop_str_from + ', transfers '
        if self.troops > 0:
            result += str(self.troops) + ' troops, '
        if self.leaders > 0:
            result += str(self.leaders) + ' leaders, '
        if self.mounts > 0:
            result += str(self.mounts) + ' mounts, '
        if self.lkp > 0:
            result += str(self.lkp) + ' lkp, '
        if self.skp > 0:
            result += str(self.skp) + ' skp '
        result += 'to ' + troop_str_to + ' on Field (' + str(self.x) + ',' + str(self.y) + '). ' + processed_str + \
                  ', ' + str(self.date)
        return result


class SplitEvent(Event):
    # Used to record the splitting of an army
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    fromArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL)
    newArmy = models.IntegerField()
    troops = models.IntegerField()
    leaders = models.IntegerField()
    mounts = models.IntegerField()
    lkp = models.IntegerField()
    skp = models.IntegerField()
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.fromArmy is None:
            troop_str_from = '*no army*'
        else:
            troop_str_from = Realm.short(self.fromArmy.realm) + ', ' + str(self.fromArmy.armyId)
        result = troop_str_from + ', splits of army  ' + str(self.newArmy) + \
               ' with ' + str(self.troops) + " troops, " + str(self.leaders) + " leaders,"
        if self.mounts > 0:
            result += str(self.mounts) + ' mounts, '
        if self.lkp > 0:
            result += str(self.lkp) + ' lkp, '
        if self.skp > 0:
            result += str(self.skp) + ' skp '
        result += ' on Field (' + str(self.x) + ',' + str(self.y) + '). ' + processed_str + ', ' + str(self.date)
        return result


class MountEvent(Event):
    # used to record both mounting and dismounting of troops
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    fromArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL)
    newArmy = models.IntegerField()
    troops = models.IntegerField()
    leaders = models.IntegerField()
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.fromArmy is None:
            troop_str_from = '*no army*'
        else:
            troop_str_from = Realm.short(self.fromArmy.realm) + ', ' + str(self.fromArmy.armyId)
        result = troop_str_from + ', mounts/unmounts  ' + str(self.newArmy) + ' with ' + str(self.troops) +\
                 " troops, and " + str(self.leaders) + " leaders,"
        result += ' on Field (' + str(self.x) + ',' + str(self.y) + '). ' + processed_str + ', ' + str(self.date)
        return result


class TurnEvent(models.Model):
    # Used to record turn change
    STATUS = (
        ("st", "start"),
        ("fi", "finished"),
    )
    turn = models.ForeignKey(TurnOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, default="st", choices=STATUS)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.turn) + ', ' + str(self.get_status_display()) + ', ' + str(self.date)


class CommentEvent(Event):
    # Used to record any other non-mechanical events
    text = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return str(self.text) + ', ' + str(self.date)


class LastSavedTimeStamp(models.Model):
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "LastSavedTimeStamps"

    def __str__(self):
        return str(self.pk) + ', ' + str(self.timeStamp)
