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
    name = models.CharField(max_length=250, null=True, blank=True)
    type = models.IntegerField()
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)
    direction = models.CharField(max_length=2, null=True, blank=True, choices=DIRECTIONS)
    firstX = models.IntegerField(null=True, blank=True)
    firstY = models.IntegerField(null=True, blank=True)
    secondX = models.IntegerField(null=True, blank=True)
    secondY = models.IntegerField(null=True, blank=True)

    def __str__(self):
        result = Realm.short(self.realm) + ' ' + str(self.name) + ' ' + str(self.type_names[self.type])
        if 0 <= self.type <= 7:
            result += ' (' + str(self.x) + ', ' + str(self.y) + ')'
        if 5 <= self.type <= 7:
            result += ' ' + str(self.direction)
        if self.type == 8:
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
    isLoadedIn = models.IntegerField(default=None, blank=True , null=True)
    STATUS_CHOICES = (("tobe", "tobe"), ("active", "active"), ("inactive", "inactive"))
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default="active",
    )

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


class MoveEvent(models.Model):
    # Used to record movement of armies
    troop = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL)
    from_x = models.IntegerField()
    from_y = models.IntegerField()
    to_x = models.IntegerField()
    to_y = models.IntegerField()
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

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


class BattleEvent(models.Model):
    # Used to record battles and their outcome
    participants = models.ManyToManyField(Troop)
    x = models.IntegerField()
    y = models.IntegerField()
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

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


class BuildEvent(models.Model):
    # Used to record builds commissioned
    #TODO: different building types need different fields
    x = models.IntegerField()
    y = models.IntegerField()
    type = models.IntegerField()
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        return '(' + str(self.x) + ', ' + str(self.y) + '), ' + str(self.type) + ', ' + processed_str + \
               ', ' + str(self.date)

class ShootEvent(models.Model):
    # Used to record all the shooting
    shooter = models.ForeignKey(Troop, on_delete=models.CASCADE, null=True)
    from_x = models.IntegerField()
    from_y = models.IntegerField()
    to_x = models.IntegerField()
    to_y = models.IntegerField()
    lkp_count = models.IntegerField()
    skp_count = models.IntegerField()
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.processed is True:
            processed_str = 'processed'
        else:
            processed_str = 'not processed'
        if self.shooter is None:
            shooter_str = '*no army*'
        else:
            shooter_str = Realm.short(self.shooter.realm) + ', ' + str(self.shooter.armyId)

        return shooter_str + ', ' + str(self.from_x) + ', ' + str(self.from_y) + '(' + str(self.to_x) + ', ' + str(self.to_y) + '), ' + str(self.lkp_count) + ', ' + str(self.skp_count) \
               + ', ' + processed_str + ', ' + str(self.date)


class RecruitmentEvent(models.Model):
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
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

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


class TreasuryEvent(models.Model):
    # Used to record changes in treasury
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    change = models.IntegerField()
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

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

class MergeEvent(models.Model):
    # Used to record the Merging of armies
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    fromArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL, related_name='+')
    toArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL, related_name='+')
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.realm) + ', army ' + str(self.fromArmy) + ', merges into ' + str(self.toArmy)

class TransferEvent(models.Model):
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
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.realm) + ', army ' + str(self.fromArmy) + ', transfers troops to ' + str(self.toArmy)

class SplitEvent(models.Model):
    # Used to record the splitting of an army
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)
    fromArmy = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL)
    newArmy = models.IntegerField()
    troops = models.IntegerField()
    leaders = models.IntegerField()
    mounts = models.IntegerField()
    lkp = models.IntegerField()
    skp = models.IntegerField()
    processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

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


class CommentEvent(models.Model):
    # Used to record any other non-mechanical events
    text = models.CharField(max_length=2000, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.text) + ', ' + str(self.date)


class LastSavedTimeStamp(models.Model):
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "LastSavedTimeStamps"

    def __str__(self):
        return str(self.pk) + ', ' + str(self.timeStamp)
