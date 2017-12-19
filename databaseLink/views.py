from django.http import HttpResponse
from django.core import serializers
import json
import time
from .models import Field, River, Building, Troop, Realm, RealmTerritory, RealmMembership, MoveEvent, BattleEvent, \
    BuildEvent, RecruitmentEvent, TurnEvent, CommentEvent, TurnOrder, LastSavedTimeStamp, SplitEvent, MergeEvent, \
    TransferEvent, MountEvent, ShootEvent
import django.middleware.csrf
import math
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from rest_framework.authtoken.models import Token
# Views for saving data from the Phoenix launcher, and views for dispensing it.

def armyData(request):
    sessionKey = request.POST.get('authorization')
    if (sessionKey == '0') | (sessionKey is None):
        all_troops_data = serializers.serialize('python', Troop.objects.filter(status="active"))
        data = [d['fields'] for d in all_troops_data]
        for d in data:
            d['count'] = -1
            d['leaders'] = -1
            d['mounts'] = -1
            d['lkp'] = -1
            d['skp'] = -1
            d['isGuard'] = False
        for d in data:
            d['realm'] = getRealmForId(d['realm'])
        returnData = json.dumps(data)
        return HttpResponse(returnData)
    else:
        user = Token.objects.get(key=sessionKey).user
        realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
        all_troops_data = serializers.serialize('python', Troop.objects.filter(status="active"))
        data = [d['fields'] for d in all_troops_data]
        if user.is_staff:  # user is SL
            pass
        elif len(realmMembership) is 0:  # user is observer
            for d in data:
                d['count'] = -1
                d['leaders'] = -1
                d['mounts'] = -1
                d['lkp'] = -1
                d['skp'] = -1
        else:  # user is realm member
            for d in data:
                if d['realm'] != realmMembership[0]['fields']['realm']:
                    d['count'] = -1
                    d['leaders'] = -1
                    d['mounts'] = -1
                    d['lkp'] = -1
                    d['skp'] = -1
                    d['isGuard'] = False
        for d in data:
            d['realm'] = getRealmForId(d['realm'])
        returnData = json.dumps(data)
        return HttpResponse(returnData)


def getLastSavedTimeStamp(request):
    stamp = LastSavedTimeStamp.objects.all().first()
    time = json.dumps(str(stamp.timeStamp))
    return HttpResponse(time)


def buildingData(request):
    all_buildings_data = serializers.serialize('python', Building.objects.all())
    data = [d['fields'] for d in all_buildings_data]
    for d in data:
        d['realm'] = getRealmForId(d['realm'])
    returnData = json.dumps(data)
    return HttpResponse(returnData)


def fieldData(request):
    all_field_data = serializers.serialize('python', Field.objects.all())
    data = [d['fields'] for d in all_field_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)


def saveFieldData(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif not user.is_staff:
        return HttpResponse(status=403)  # Access denied. You have to be SL to do this.
    else:
        currentMapData = Field.objects.all()
        mapdata = request.POST.get("map")
        listOfData = mapdata.split(";")
        for listItem in listOfData:
            typeXY = listItem.split(",")
            currentMapData.filter(x=typeXY[1]).filter(y=typeXY[2]).delete()
            field = Field()
            field.type = typeXY[0]
            field.x = typeXY[1]
            field.y = typeXY[2]
            field.save()
        update_timestamp()
        return HttpResponse(status=200)  # Success.


def update_timestamp():
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()


def saveRiverData(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif not user.is_staff:
        return HttpResponse(status=403)  # Access denied. You have to be SL to do this.
    else:
        currentRiverData = River.objects.all()
        riverData = request.POST.get("river")
        listOfData = riverData.split(";")
        riversToSave = [];
        for listItem in listOfData:
            xyxy = listItem.split(",")
            currentRiverData.filter(firstX=xyxy[0]).filter(firstY=xyxy[1]).filter(secondX=xyxy[2]).\
                filter(secondY=xyxy[3]).delete()
            print("deleted")
            river = River()
            river.firstX = xyxy[0]
            river.firstY = xyxy[1]
            river.secondX = xyxy[2]
            river.secondY = xyxy[3]
            river.save()
            riversToSave.append(river.pk)
        currentRiverData = River.objects.all()
        currentRiverData.exclude(pk__in = riversToSave).delete()
        update_timestamp()
        return HttpResponse(status=200)  # Success.


def saveBuildingData(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif not user.is_staff:
        return HttpResponse(status=403)  # Access denied. You have to be SL to do this.
    else:
        currentBuildingData = Building.objects.all()
        buildingData = request.POST.get("buildings")
        listOfData = buildingData.split(";")
        for listItem in listOfData:
            building = listItem.split(",")
            for listItem in listOfData:
                building = listItem.split(",")
                buildingLength = len(building)
                if building[buildingLength - 1] == "true":
                    if int(building[0]) <= 4:
                        newBuilding = currentBuildingData.exclude(type=5).exclude(type=6).exclude(type=7).exclude(
                            type=8) \
                            .filter(realm=building[1]).filter(x=building[2]).filter(y=building[3])
                        if len(newBuilding) == 1:
                            newBuilding = newBuilding[0]
                        else:
                            newBuilding = Building()
                        newBuilding.type = building[0]
                        newBuilding.realm = Realm.objects.get(tag=building[1])
                        newBuilding.x = building[2]
                        newBuilding.y = building[3]
                        newBuilding.save()
                    elif int(building[0]) <= 7:
                        newBuilding = currentBuildingData.filter(type=building[0]).filter(realm=building[1]) \
                            .filter(x=building[2]).filter(y=building[3]).filter(direction=building[4])
                        if len(newBuilding) == 1:
                            newBuilding = newBuilding[0]
                        else:
                            newBuilding = Building()
                        newBuilding.type = building[0]
                        newBuilding.realm = Realm.objects.get(tag=building[1])
                        newBuilding.x = building[2]
                        newBuilding.y = building[3]
                        newBuilding.direction = building[4]
                        newBuilding.save()
                    elif int(building[0]) == 8:
                        newBuilding = currentBuildingData.filter(type=8).filter(realm=building[1]).filter(
                            firstX=building[2]) \
                            .filter(firstY=building[3]).filter(secondX=building[4]).filter(secondY=building[5])
                        if len(newBuilding) == 1:
                            newBuilding = newBuilding[0]
                        else:
                            newBuilding = Building()
                        newBuilding.type = building[0]
                        newBuilding.realm = Realm.objects.get(tag=building[1])
                        newBuilding.firstX = building[2]
                        newBuilding.firstY = building[3]
                        newBuilding.secondX = building[4]
                        newBuilding.secondY = building[5]
                        newBuilding.save()
                elif building[buildingLength - 1] == "false":
                    if int(building[0]) <= 4:
                        currentBuildingData.exclude(type=5).exclude(type=6).exclude(type=7).exclude(type=8) \
                            .filter(realm=building[1]).filter(x=building[2]).filter(y=building[3]).delete()
                        print("deleted")
                    elif int(building[0]) <= 7:
                        currentBuildingData.exclude(type=0).exclude(type=1).exclude(type=2).exclude(type=3) \
                            .exclude(type=4).exclude(type=8).filter(realm=building[1]).filter(x=building[2]) \
                            .filter(y=building[3]).filter(direction=building[4]).delete()
                        print("deleted")
                    elif int(building[0]) == 8:
                        currentBuildingData.filter(type=8).filter(realm=building[1]).filter(firstX=building[2]) \
                            .filter(firstY=building[3]).filter(secondX=building[4]).filter(secondY=building[5]).delete()
                        print("deleted")
        update_timestamp()
        return HttpResponse(status=200)  # Success.


def saveArmyData(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif not user.is_staff:
        return HttpResponse(status=403)  # Access denied. You have to be SL to do this.
    else:
        currentArmyData = Troop.objects.all()
        # armydata = request.POST.get("armies")
        listOfData = json.loads(request.POST['armies'])
        armiesToSave = []
        for listItem in listOfData:
            # axyol = listItem.split(",")
            # Army axyol[0-5], X = axyol[6], Y = axyol[7], Owner = axyol[8], isLoaded in axyol[9]
            findArmyInDB = currentArmyData.filter(armyId=listItem['armyId']).filter(status="active")\
                .filter(realm=Realm.objects.get(tag=listItem['owner']).pk)
            if len(findArmyInDB) > 0:
                army = findArmyInDB[0]
            else:
                army = Troop()
            army.armyId = listItem['armyId']
            army.count = listItem['count']
            army.leaders = listItem['leaders']
            army.lkp = listItem['lkp']
            army.skp = listItem['skp']
            army.mounts = listItem['mounts']
            army.x = listItem['x']
            army.y = listItem['y']
            army.realm = Realm.objects.get(tag=listItem['owner'])
            army.movementPoints = listItem['movementPoints']
            army.heightPoints = listItem['heightPoints']
            if listItem['isLoadedIn'] == "null":
                army.isLoadedIn = None
            else:
                army.isLoadedIn = listItem['isLoadedIn']
            army.save()
            armiesToSave.append(army.pk)
        currentArmyData = Troop.objects.all()
        troopsToSetInactive = currentArmyData.exclude(pk__in=armiesToSave)
        for potentiallyInactive in troopsToSetInactive:
            status = potentiallyInactive.status
            if status != "tobe":
                potentiallyInactive.status = "inactive"
                potentiallyInactive.save()
        update_timestamp()
        return HttpResponse(status=200)  # Success.


def saveBorderData(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif not user.is_staff:
        return HttpResponse(status=403)  # Access denied. You have to be SL to do this.
    else:
        new_border_data = json.loads(request.POST['borders'])
        realms = Realm.objects.all()
        for realm in realms:
            new_realm_borders = filter(lambda x: x['tag'] == realm.tag, new_border_data)[0]['land']
            old_realm_borders = RealmTerritory.objects.filter(realm=realm)
            for field in old_realm_borders:
                if not ([field.x, field.y] in new_realm_borders):
                    field.delete()
            for field in new_realm_borders:
                if not filter(lambda old_field: old_field.x == field[0] and old_field.y == field[1], old_realm_borders):
                    realm_field = RealmTerritory()
                    realm_field.realm = realm
                    realm_field.x = field[0]
                    realm_field.y = field[1]
                    realm_field.save()
        update_timestamp()
        return HttpResponse(status=200)  # Success.


def getBorderData(request):
    all_border_data = [d['fields'] for d in serializers.serialize('python', RealmTerritory.objects.all())]
    realms = [(d['pk'], d['fields']['tag']) for d in serializers.serialize('python', Realm.objects.filter(active=True))]
    sorted_borders = [[r[1], [[d['x'], d['y']] for d in
                              list(filter(lambda x: x['realm'] == r[0], all_border_data))]] for r in realms]
    return HttpResponse(json.dumps([{'tag': d[0], 'land': d[1]} for d in sorted_borders]))


def getCurrentTurn(request):
    latest_turn = TurnEvent.objects.filter(date__isnull=False).latest('date')
    serialized_turn = [d['fields'] for d in serializers.serialize('python', [latest_turn], fields=('turn', 'status'))]
    turn_order = [d['fields'] for d in
                  serializers.serialize('python', [TurnOrder.objects.get(id=[d['turn'] for d in
                                                                             serialized_turn][0])])][0]
    realm_in_turn = getRealmForId(turn_order)
    return HttpResponse(json.dumps({
        'turn': turn_order['turnNumber'],
        'realm': realm_in_turn,
        'status': [d['status'] for d in serialized_turn][0]
    }), content_type='application/json')


def getRiverData(request):
    all_river_data = serializers.serialize('python', River.objects.all())
    data = [d['fields'] for d in all_river_data]
    return HttpResponse(json.dumps(data))


def getCSRFToken(request): ## TODO: funktioniert noch nicht
    tokenToReturn = json.dumps(django.middleware.csrf.get_token(request))
    return HttpResponse(tokenToReturn)


class UserFormView(View):
    form_class = UserForm
    template_name = 'databaseLink/accountcreation_form.html'

    #  display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #  process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #  cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #  returns User object if credentials are correct (they should be at this stage)
            user = authenticate(username=username, password=password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('http://h2610265.stratoserver.net')


def loginView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            try:
                Token.objects.get(user=user).delete()
            except:
                pass
            # check if user is a member of a realm, a sl or just a guest
            realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
            if user.is_staff:
                group = 'sl'
            elif len(realmMembership) > 0:
                rm = realmMembership[0]['fields']['realm']
                group = serializers.serialize('python', Realm.objects.filter(pk=rm))[0]['fields']['tag']
            else:
                group = 'guest'
            # Add the token to the return serialization
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'group': group
            }
            returnData = json.dumps(data)
            return HttpResponse(returnData)
        else:
            return HttpResponse('This account is not Active.')
    else:
        return HttpResponse('Username/password combination invalid.')


def postNextTurn(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        try:
            nextTurn()
            return getCurrentTurn(None)
        except TurnOrderException:
            return HttpResponse(status=521)  # Turn Order ran out. You should fill it! (custom status code)
    else:
        latestTurn = TurnEvent.objects.filter(date__isnull=False).latest('date')
        serializedTurn = [d['fields'] for d in serializers.serialize('python', [latestTurn], fields=('turn', 'status'))]
        turnOrder = [d['fields'] for d in
                     serializers.serialize('python', [TurnOrder.objects.get(id=[d['turn'] for d in
                                                                                serializedTurn][0])])][0]
        status = [d['status'] for d in serializedTurn][0]
        if (getRealmForId(turnOrder) is not None) & \
                (turnOrder['realm'] == realmMembership[0]['fields']['realm']) & (status == 'st'):
            try:
                nextTurn()
                update_timestamp()
                return getCurrentTurn(None)
            except TurnOrderException:
                return HttpResponse(status=520)  # Turn Order ran out. Tell SL to fill it! (custom status code)
        else:
            return HttpResponse(status=403)  # Access denied. You can only end your own turn.


def deleteEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    if(user.is_staff):
        event_id = request.POST.get('eventId')
        event_type = request.POST.get('eventType')
        if event_type == 'move':
            MoveEvent.objects.filter(id=event_id).delete()
        elif event_type == 'battle':
            BattleEvent.objects.filter(id=event_id).delete()
        elif event_type == 'split':
            SplitEvent.objects.filter(id=event_id).delete()
        elif event_type == 'merge':
            MergeEvent.objects.filter(id=event_id).delete()
        elif event_type == 'transfer':
            TransferEvent.objects.filter(id=event_id).delete()
        elif event_type == 'shoot':
            ShootEvent.objects.filter(id=event_id).delete()
        elif event_type == 'mount':
            MountEvent.objects.filter(id=event_id).delete()
        # update_timestamp()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)  # Access denied. You have to be a SL to do this.


def checkEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    if(user.is_staff):
        event_id = request.POST.get('eventId')
        event_type = request.POST.get('eventType')
        # TODO: Do this for all other types of events (when you come around to using them).
        if event_type == 'move':
            me = MoveEvent.objects.filter(id=event_id)[0]
            me.processed = True
            me.save()
        elif event_type == 'battle':
            be = BattleEvent.objects.filter(id=event_id)[0]
            be.processed = True
            be.save()
        elif event_type == 'split':
            be = SplitEvent.objects.filter(id=event_id)[0]
            toArmy = Troop.objects.filter(armyId=be.newArmy).get(realm=be.realm)
            toArmy.status = 'active'
            toArmy.save()
            be.processed = True
            be.save()
        elif event_type == 'merge':
            be = MergeEvent.objects.filter(id=event_id)[0]
            be.processed = True
            be.save()
        elif event_type == 'transfer':
            be = TransferEvent.objects.filter(id=event_id)[0]
            be.processed = True
            be.save()
        elif event_type == 'shoot':
            be = ShootEvent.objects.filter(id=event_id)[0]
            be.processed = True
            be.save()
        elif event_type == 'mount':
            be = MountEvent.objects.filter(id=event_id)[0]
            toArmy = Troop.objects.filter(armyId=be.newArmy).get(realm=be.realm)
            toArmy.status = 'active'
            toArmy.save()
            be.processed = True
            be.save()
        # update_timestamp()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)  # Access denied. You have to be a SL to do this.


def getPendingEvents(request):
    pending_move_events = serializers.serialize('python', MoveEvent.objects.filter(processed=False))
    pending_battle_events = serializers.serialize('python', BattleEvent.objects.filter(processed=False))
    pending_split_events = serializers.serialize('python', SplitEvent.objects.filter(processed=False))
    pending_merge_events = serializers.serialize('python', MergeEvent.objects.filter(processed=False))
    pending_tansfer_events = serializers.serialize('python', TransferEvent.objects.filter(processed=False))
    pending_shoot_events = serializers.serialize('python', ShootEvent.objects.filter(processed=False))
    pending_mount_events = serializers.serialize('python', MountEvent.objects.filter(processed=False))
    # TODO: Do this for all other types of events (when you come around to using them).
    json_events = []
    for e in pending_move_events:
        troops = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['troop'])))
        if len(troops) > 0:
            id = troops[0]['fields']['armyId']
            realm = getRealmForId(troops[0]['fields'])
        else:
            id = '*none*'
            realm = '*none*'
        json_events.append({
            'type': 'move',
            'content': {
                'armyId': id,
                'realm': realm,
                'fromX': e['fields']['from_x'],
                'fromY': e['fields']['from_y'],
                'toX': e['fields']['to_x'],
                'toY': e['fields']['to_y']
            },
            'pk': e['pk']
        })
    for e in pending_battle_events:
        json_events.append({
                'type': 'battle',
                'content': {
                    'participants': getParticipants(e['fields']['participants']),
                    'x': e['fields']['x'],
                    'y': e['fields']['y']
                },
                'pk': e['pk']
            })
    for e in pending_merge_events:
        fromArmy = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['fromArmy'])))
        if len(fromArmy) > 0:
            id1 = fromArmy[0]['fields']['armyId']
        else:
            id1 = '*none*'
        toArmy = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['toArmy'])))
        if len(toArmy) > 0:
            id2 = toArmy[0]['fields']['armyId']
        else:
            id2 = '*none*'
        json_events.append({
            'type': 'merge',
            'content': {
                'realm': e['fields']['realm'],
                'fromArmy': id1,
                'toArmy': id2,
                'x': e['fields']['x'],
                'y': e['fields']['y']
            },
            'pk': e['pk']
        })
    for e in pending_tansfer_events:
        fromArmy = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['fromArmy'])))
        if len(fromArmy) > 0:
            id1 = fromArmy[0]['fields']['armyId']
        else:
            id1 = '*none*'
        toArmy = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['toArmy'])))
        if len(toArmy) > 0:
            id2 = toArmy[0]['fields']['armyId']
        else:
            id2 = '*none*'
        json_events.append({
            'type': 'transfer',
            'content': {
                'realm': e['fields']['realm'],
                'fromArmy': id1,
                'toArmy': id2,
                'armyFromType': e['fields']['armyFromType'],
                'armyToType': e['fields']['armyToType'],
                'troops': e['fields']['troops'],
                'leaders': e['fields']['leaders'],
                'mounts': e['fields']['mounts'],
                'lkp': e['fields']['lkp'],
                'skp': e['fields']['skp'],
                'x': e['fields']['x'],
                'y': e['fields']['y']
            },
            'pk': e['pk']
        })
    for e in pending_split_events:
        fromArmy = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['fromArmy'])))
        if len(fromArmy) > 0:
            id1 = fromArmy[0]['fields']['armyId']
        else:
            id1 = '*none*'
        json_events.append({
            'type': 'split',
            'content': {
                'realm': e['fields']['realm'],
                'fromArmy': id1,
                'newArmy': e['fields']['newArmy'],
                'troops': e['fields']['troops'],
                'leaders': e['fields']['leaders'],
                'mounts': e['fields']['mounts'],
                'lkp': e['fields']['lkp'],
                'skp': e['fields']['skp'],
                'x': e['fields']['x'],
                'y': e['fields']['y']
            },
            'pk': e['pk']
        })
    for e in pending_mount_events:
        fromArmy = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['fromArmy'])))
        if len(fromArmy) > 0:
            id1 = fromArmy[0]['fields']['armyId']
        else:
            id1 = '*none*'
        json_events.append({
            'type': 'mount',
            'content': {
                'realm': e['fields']['realm'],
                'fromArmy': id1,
                'newArmy': e['fields']['newArmy'],
                'troops': e['fields']['troops'],
                'leaders': e['fields']['leaders'],
                'x': e['fields']['x'],
                'y': e['fields']['y']
            },
            'pk': e['pk']
        })
    for e in pending_shoot_events:
        shootArmy = serializers.serialize('python', Troop.objects.filter(id=(e['fields']['shooter'])))
        if len(shootArmy) > 0:
            id1 = shootArmy[0]['fields']['armyId']
        else:
            id1 = '*none*'
        json_events.append({
            'type': 'shoot',
            'content': {
                'armyId': id1,
                'realm': e['fields']['realm'],
                'LKPcount': e['fields']['lkp_count'],
                'SKPcount': e['fields']['skp_count'],
                'toX': e['fields']['to_x'],
                'toY': e['fields']['to_y'],
                'target': e['fields']['target'],
                'fromX': e['fields']['from_x'],
                'fromY': e['fields']['from_y']
            },
            'pk': e['pk']
        })
    return HttpResponse(json.dumps(json_events))


def getParticipants(armyPKs):
    result = []
    for a in armyPKs:
        army = serializers.serialize('python', Troop.objects.filter(id=a))[0]['fields']
        result.append({
            'armyId': army['armyId'],
            'realm': getRealmForId(army)
        })
    return result


def postMoveEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
    event = json.loads(request.POST.get('content'))
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        # enter into db
        return enterMoveEvent(event)
    else:
        # check if user is of correct realm, then enter into db
        if getRealmForId(realmMembership[0]['fields']) == event['realm']:
            return enterMoveEvent(event)
        else:
            return HttpResponse(status=403)  # Access denied. You can only move your own army.


def postShootEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
    event = json.loads(request.POST.get('content'))
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        # enter into db
        return enterShootEvent(event)
    else:
        # check if user is of correct realm, then enter into db
        if getRealmForId(realmMembership[0]['fields']) == event['realm']:
            return enterShootEvent(event)
        else:
            return HttpResponse(status=403)  # Access denied. You can only move your own army.


def postBattleEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    event = json.loads(request.POST.get('content'))
    participants = event['participants']
    armies = list()
    for p in participants:
        pRealm = Realm.objects.filter(tag=p['realm'])[0]
        participant = Troop.objects.filter(armyId=p['armyId']).filter(realm=pRealm)[0]
        armies.append(participant)
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        # enter into db
        return enterBattleEvent(event, armies)
    else:
        # check if user is of correct realm, then enter into db
        allowed = False
        realmMembership = serializers.serialize('python',
                                                RealmMembership.objects.filter(user=user))[0]['fields']['realm']
        for x in armies:  # check if at least one involved army belongs to an issuing player
            if x.realm.pk == realmMembership:
                allowed = True
        if allowed:
            return enterBattleEvent(event, armies)
        else:
            return HttpResponse(status=403)  # Access denied. You can only send battle events involving your armies.

def postMergeEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    event = json.loads(request.POST.get('content'))
    realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        # enter into db
        print("user is staff:")
        return enterMergeEvent(event)
    else:
        # check if user is of correct realm, then enter into db
        if getRealmForId(realmMembership[0]['fields']) == event['realm']:
            print("user is fitting realm:")
            return enterMergeEvent(event)
        else:
            print("user is wrong realm:")
            return HttpResponse(status=403)  # Access denied. You can only move your own army.


def postTransferEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    event = json.loads(request.POST.get('content'))
    realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        # enter into db
        print("user is staff:")
        return enterTransferEvent(event)
    else:
        # check if user is of correct realm, then enter into db
        if getRealmForId(realmMembership[0]['fields']) == event['realm']:
            print("user is fitting realm:")
            return enterTransferEvent(event)
        else:
            print("user is wrong realm:")
            return HttpResponse(status=403)  # Access denied. You can only move your own army.

def postSplitEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    event = json.loads(request.POST.get('content'))
    realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        # enter into db
        print("user is staff:")
        return enterSplitEvent(event)
    else:
        # check if user is of correct realm, then enter into db
        if getRealmForId(realmMembership[0]['fields']) == event['realm']:
            print("user is fitting realm:")
            return enterSplitEvent(event)
        else:
            print("user is wrong realm:")
            return HttpResponse(status=403)  # Access denied. You can only move your own army.

def enterMergeEvent(event):
    realm = serializers.serialize('python', Realm.objects.filter(tag=event['realm']))
    if len(realm) == 0:
        return HttpResponse(status=400)  # Invalid input. Realm given does not exist.
    fromArmyId = Troop.objects.filter(armyId=event['fromArmyId']).filter(realm=realm[0]['pk'])
    if len(fromArmyId) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    toArmyId = Troop.objects.filter(armyId=event['toArmyId']).filter(realm=realm[0]['pk'])
    if len(toArmyId) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    me = MergeEvent(realm=Realm.objects.get(tag=event['realm']), fromArmy=fromArmyId[0], toArmy=toArmyId[0],
                    x = event['x'], y = event['y'])
    me.save()
    update_timestamp()
    return HttpResponse(status=200)

def enterTransferEvent(event):
    realm = serializers.serialize('python', Realm.objects.filter(tag=event['realm']))
    if len(realm) == 0:
        return HttpResponse(status=400)  # Invalid input. Realm given does not exist.
    fromArmyId = Troop.objects.filter(armyId=event['fromArmyId']).filter(realm=realm[0]['pk'])
    if len(fromArmyId) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    toArmyId = Troop.objects.filter(armyId=event['toArmyId']).filter(realm=realm[0]['pk'])
    if len(toArmyId) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    te = TransferEvent(realm=Realm.objects.get(tag=event['realm']), fromArmy=fromArmyId[0], toArmy=toArmyId[0],
                       troops=event['troops'], leaders=event['leaders'], mounts=event['mounts'],
                       skp=event['skp'], lkp=event['lkp'], armyFromType=math.floor(event['fromArmyId']/100),
                       armyToType=math.floor(event['toArmyId'] / 100),
                       x = event['x'], y = event['y'])
    te.save()
    update_timestamp()
    return HttpResponse(status=200)

def postMountEvent(request):
    sessionKey = request.POST.get('authorization')
    user = Token.objects.get(key=sessionKey).user
    event = json.loads(request.POST.get('content'))
    realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
    if (sessionKey == '0') | (sessionKey is None):
        return HttpResponse(status=401)  # Authorisation failure. Please log in.
    elif user.is_staff:
        # enter into db
        print("user is staff:")
        return enterMountEvent(event)
    else:
        # check if user is of correct realm, then enter into db
        if getRealmForId(realmMembership[0]['fields']) == event['realm']:
            print("user is fitting realm:")
            return enterMountEvent(event)
        else:
            print("user is wrong realm:")
            return HttpResponse(status=403)  # Access denied. You can only move your own army.

def enterSplitEvent(event):
    realm = serializers.serialize('python', Realm.objects.filter(tag=event['realm']))
    if len(realm) == 0:
        return HttpResponse(status=400)  # Invalid input. Realm given does not exist.
    fromArmyId = Troop.objects.filter(armyId=event['fromArmyId']).filter(realm=realm[0]['pk'])
    if len(fromArmyId) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    se = SplitEvent(realm=Realm.objects.get(tag=event['realm']), fromArmy=fromArmyId[0], newArmy=event['newArmysId'],
                    troops=event['troops'], leaders=event['leaders'], mounts=event['mounts'],
                    skp=event['skp'], lkp=event['lkp'], x = event['x'], y = event['y'])
    newArmy = Troop(realm=Realm.objects.get(tag=event['realm']), armyId=event['newArmysId'], count=event['troops'],
                    leaders=event['leaders'], mounts=event['mounts'], skp=event['skp'], lkp=event['lkp'],
                    x=event['x'], y=event['y'], movementPoints=fromArmyId[0].movementPoints,
                    heightPoints=fromArmyId[0].heightPoints, status='tobe')
    se.save()
    newArmy.save()
    update_timestamp()
    return HttpResponse(status=200)

def enterMoveEvent(event):
    realm = serializers.serialize('python', Realm.objects.filter(tag=event['realm']))
    if len(realm) == 0:
        return HttpResponse(status=400)  # Invalid input. Realm given does not exist.
    army = Troop.objects.filter(armyId=event['armyId']).filter(realm=realm[0]['pk'])
    if len(army) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    me = MoveEvent(troop=army[0], from_x=event['fromX'], from_y=event['fromY'], to_x=event['toX'], to_y=event['toY'])
    me.save()
    # update_timestamp()
    return HttpResponse(status=200)

def enterShootEvent(event):
    realm = serializers.serialize('python', Realm.objects.filter(tag=event['realm']))
    if len(realm) == 0:
        return HttpResponse(status=400)  # Invalid input. Realm given does not exist.
    army = Troop.objects.filter(armyId=event['shooterID']).filter(realm=realm[0]['pk'])
    if len(army) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    me = ShootEvent(shooter=army[0],realm=Realm.objects.get(tag=event['realm']), lkp_count=event['LKPcount'], skp_count=event['SKPcount'], to_x=event['toX'], to_y=event['toY'],
                    target=event['target'], from_x=event['fromX'], from_y=event['fromY'])
    me.save()
    # update_timestamp()
    return HttpResponse(status=200)

def enterBattleEvent(event, armies):
    partips = list()
    for x in armies:
        partips.append(x.id)
    be = BattleEvent(x=event['x'], y=event['y'])
    be.save()
    be.participants = partips
    # update_timestamp()
    return HttpResponse(status=200)

def enterMountEvent(event):
    realm = serializers.serialize('python', Realm.objects.filter(tag=event['realm']))
    print("before realm")
    if len(realm) == 0:
        return HttpResponse(status=400)  # Invalid input. Realm given does not exist.
    print("realm exists")
    print("before from army")
    print("fromArmyId = " + str(event['fromArmyId']) + ", realm = " + str(realm[0]['pk']))
    fromArmyId = Troop.objects.filter(armyId=event['fromArmyId']).filter(realm=realm[0]['pk'])
    print(fromArmyId)
    if len(fromArmyId) == 0:
        return HttpResponse(status=400)  # Invalid input. Troop does not exist.
    print("from army exists")
    mounts = 0
    if (fromArmyId[0].armyId >= 200) and (fromArmyId[0].armyId < 300):
        mounts = event['troops']
        print("mounts = " + mounts)
    me = MountEvent(realm=Realm.objects.get(tag=event['realm']), fromArmy=fromArmyId[0], newArmy=event['newArmysId'],
                    troops=event['troops'], leaders=event['leaders'], x = event['x'], y = event['y'])
    newArmy = Troop(realm=Realm.objects.get(tag=event['realm']), armyId=event['newArmysId'], count=event['troops'],
                    leaders=event['leaders'], mounts=mounts, skp=0, lkp=0, x=event['x'], y=event['y'],
                    movementPoints=fromArmyId[0].movementPoints, heightPoints=fromArmyId[0].heightPoints, status='tobe')
    print(newArmy)
    me.save()
    newArmy.save()
    print("newArmy saved")
    update_timestamp()
    return HttpResponse(status=200)

def nextTurn():
    latestTurn = TurnEvent.objects.filter(date__isnull=False).latest('date')
    serializedTurn = [d['fields'] for d in serializers.serialize('python', [latestTurn], fields=('turn', 'status'))]
    currentTurnOrderElement = [d['fields'] for d in
                               serializers.serialize('python', [TurnOrder.objects.get(id=[d['turn'] for d in
                                                                                          serializedTurn][0])])][0]
    turnOrder = currentTurnOrderElement['turnOrder']
    turnNumber = currentTurnOrderElement['turnNumber']
    status = [d['status'] for d in serializedTurn][0]
    if status == 'st':
        if turnOrder == 0:
            newstatus = 'st'
        else:
            newstatus = 'fi'
    else:
        newstatus = 'st'

    if newstatus == 'st':
        newturn = TurnOrder.objects.filter(turnNumber=turnNumber, turnOrder=(turnOrder+1))
    else:
        newturn = TurnOrder.objects.filter(turnNumber=turnNumber, turnOrder=turnOrder)

    if len(newturn) == 0:
        newturn = TurnOrder.objects.filter(turnNumber=(turnNumber+1), turnOrder=0)
    if len(newturn) == 0:
        raise TurnOrderException
    te = TurnEvent(status=newstatus, turn=newturn[0])
    te.save()


def getRealms(request):
    all_realm_data = serializers.serialize('python', Realm.objects.all())
    data = [d['fields'] for d in all_realm_data]
    return HttpResponse(json.dumps(data))


def getRealmForId(d):
    if type(d) is int:
        return Realm.objects.get(id=d).tag
    elif d['realm'] is None:
        return None
    else:
        return Realm.objects.get(id=[d][0]['realm']).tag


class TurnOrderException(Exception):
    """End of turn orders reached. Generate more turn orders."""
    pass
