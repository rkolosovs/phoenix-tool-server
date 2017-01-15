from django.http import HttpResponse
from django.core import serializers
import json
from .models import Field, River, Building, Troop, Realm, RealmTerritory, RealmMembership, MoveEvent, BattleEvent, \
    BuildEvent, RecruitmentEvent, TurnEvent, CommentEvent, TurnOrder, LastSavedTimeStamp
import django.middleware.csrf
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from rest_framework.authtoken.models import Token
## Views for saving data from the Phoenix launcher, and views for dinspensing it.


def armyData(request):
    sessionKey = request.POST.get('authorization')
    if (sessionKey == '0') | (sessionKey is None):
        all_troops_data = serializers.serialize('python', Troop.objects.all())
        data = [d['fields'] for d in all_troops_data]
        for d in data:
            d['count'] = -1
            d['leaders'] = -1
            d['mounts'] = -1
            d['lkp'] = -1
            d['skp'] = -1
        returnData = json.dumps(data)
        return HttpResponse(returnData)
    else:
        user = Token.objects.get(key=sessionKey).user
        realmMembership = serializers.serialize('python', RealmMembership.objects.filter(user=user))
        all_troops_data = serializers.serialize('python', Troop.objects.all())
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
        returnData = json.dumps(data)
        return HttpResponse(returnData)


def buildingData(request):
    all_buildings_data = serializers.serialize('python', Building.objects.all())
    data = [d['fields'] for d in all_buildings_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)


def fieldData(request):
    all_field_data = serializers.serialize('python', Field.objects.all())
    data = [d['fields'] for d in all_field_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)


def saveFieldData(request):
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
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()
    return HttpResponse("done")


def saveRiverData(request):
    currentRiverData = River.objects.all()
    riverData = request.POST.get("river")
    listOfData = riverData.split(";")
    for listItem in listOfData:
        xyxy = listItem.split(",")
        currentRiverData.filter(firstX=xyxy[0]).filter(firstY=xyxy[1]).filter(secondX=xyxy[2]).filter(secondY=xyxy[3]).delete()
        print("deleted")
        river = River()
        river.firstX = xyxy[0]
        river.firstY = xyxy[1]
        river.secondX = xyxy[2]
        river.secondY = xyxy[3]
        river.save()
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()
    return HttpResponse("done")


def saveBuildingData(request):
    currentBuildingData = Building.objects.all()
    buildingData = request.POST.get("buildings")
    listOfData = buildingData.split(";")
    for listItem in listOfData:
        building = listItem.split(",")
        if int(building[0]) <= 4:
            currentBuildingData.filter(type=building[0]).filter(reich=building[1]).filter(x=building[2])\
                .filter(y=building[3]).delete()
            print("deleted")
            newBuilding = Building()
            newBuilding.type = building[0]
            newBuilding.reich = Realm.objects.get(pk=building[1])
            newBuilding.x = building[2]
            newBuilding.y = building[3]
            newBuilding.save()
        elif int(building[0]) <= 7:
            currentBuildingData.filter(type=building[0]).filter(reich=building[1]).filter(x=building[2])\
                .filter(y=building[3]).filter(direction=building[4]).delete()
            print("deleted")
            newBuilding = Building()
            newBuilding.type = building[0]
            newBuilding.reich = Realm.objects.get(pk=building[1])
            newBuilding.x = building[2]
            newBuilding.y = building[3]
            newBuilding.direction = building[4]
            newBuilding.save()
        elif int(building[0]) <= 8:
            currentBuildingData.filter(type=building[0]).filter(reich=building[1]).filter(firstX=building[2])\
                .filter(firstY=building[3]).filter(secondX=building[4]).filter(secondY=building[5]).delete()
            print("deleted")
            newBuilding = Building()
            newBuilding.type = building[0]
            newBuilding.reich = Realm.objects.get(pk= building[1])
            newBuilding.firstX = building[2]
            newBuilding.firstY = building[3]
            newBuilding.secondX = building[4]
            newBuilding.secondY = building[5]
            newBuilding.save()
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()
    return HttpResponse("done")


def saveArmyData(request):
    sessionKey = request.POST.get('authorization')
    if (sessionKey == '0') | (sessionKey is None):
        pass
    else:
        user = Token.objects.get(key=sessionKey).user
        reich = RealmMembership.objects.get(user=user).reich
        currentArmyData = Troop.objects.all()
        armydata = request.POST.get("armies")
        listOfData = armydata.split(";")
        for listItem in listOfData:
            axyo = listItem.split(",")  # Army axyo[0-5], X = axyo[6], Y = axyo[7], Owner = axyo[8]
            if reich == Realm.objects.get(pk=axyo[8]):
                print(listItem)
                currentArmyData.filter(armyId=axyo[0]).filter(reich=Realm.objects.get(pk=axyo[8])).delete()
                print("deleted")
                army = Troop()
                army.armyId = axyo[0]
                army.count = axyo[1]
                army.leaders = axyo[2]
                army.lkp = axyo[3]
                army.skp = axyo[4]
                army.mounts = axyo[5]
                army.x = axyo[6]
                army.y = axyo[7]
                army.reich = Realm.objects.get(pk=axyo[8])
                army.save()
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()
    return HttpResponse("done")


def saveBorderData(request):
    currentBorderData = RealmTerritory.objects.all()
    borderdata = request.POST.get("borders")
    listOfData = borderdata.split(";")
    for listItem in listOfData:
        reichfieldlist = listItem.split(":")
        owner = Realm.objects.get(name=reichfieldlist[0])
        fields = reichfieldlist[1].split(",")
        for field in fields:
            xy = field.split("/")
            currentBorderData.filter(x=xy[0]).filter(y=xy[1]).delete()
            print("deleted")
            reichsgebiet = RealmTerritory()
            reichsgebiet.reich = owner
            reichsgebiet.x = xy[0]
            reichsgebiet.y = xy[1]
            reichsgebiet.save()
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()
    return HttpResponse("done")


def getBorderData(request):
    all_border_data = serializers.serialize('python', RealmTerritory.objects.all())
    data = [d['fields'] for d in all_border_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)


def getCurrentTurn(request):
    latestTurn = TurnEvent.objects.filter(date__isnull=False).latest('date')
    serializedTurn = [d['fields'] for d in serializers.serialize('python', [latestTurn], fields=('turn', 'status'))]
    turnOrder = [d['fields'] for d in serializers.serialize('python', [TurnOrder.objects.get(id=[d['turn'] for d in serializedTurn][0])])][0]
    # TODO: handle realm is None
    print(turnOrder)
    realmInTurn = getRealmForId(turnOrder)
    # output = turnOrder['turnNumber'] + realmInTurn + [d['status'] for d in serializedTurn]
    return HttpResponse(json.dumps({
        'turn': turnOrder['turnNumber'],
        'realm': realmInTurn,
        'status': [d['status'] for d in serializedTurn][0]
    }), content_type='application/json')


def getRiverData(request):
    all_river_data = serializers.serialize('python', River.objects.all())
    data = [d['fields'] for d in all_river_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)


def getCSRFToken(request): ## TODO: funktioniert noch nicht
    tokenToReturn = json.dumps(django.middleware.csrf.get_token(request))
    return HttpResponse(tokenToReturn)


class UserFormView(View):
    form_class = UserForm
    template_name = 'databaseLink/accountcreation_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #returns User object if credentials are correct (they should be at this stage)
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


def getRealmForId(d):
    if d['realm'] is None:
        return None
    else:
        return Realm.objects.get(id=[d][0])['fields']['tag']
