from django.http import HttpResponse
from django.core import serializers
import json
from .models import Field, Fluesse, Ruestgueter, Truppen, Reich, Reichsgebiet, Reichszugehoerigkeit, LastSavedTimeStamp
import django.middleware.csrf
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from rest_framework.authtoken.models import Token
## Views for saving data from the Phoenix launcher, and views for dispensing it.

def armyData(request):
    sessionKey = request.POST.get('authorization')
    if((sessionKey == '0' )|(sessionKey == None)):
        all_troops_data = serializers.serialize('python', Truppen.objects.all())
        data = [d['fields'] for d in all_troops_data]
        for d in data:
            d['count']= -1
            d['leaders']= -1
            d['mounts']= -1
            d['lkp']= -1
            d['skp']= -1
            d['isGuard']= False
        returnData = json.dumps(data)
        return HttpResponse(returnData)
    else:
        user = Token.objects.get(key = sessionKey).user
        reich = Reichszugehoerigkeit.objects.get(user = user).reich
        all_troops_data = serializers.serialize('python', Truppen.objects.all())
        data = [d['fields'] for d in all_troops_data]
        if(user.is_staff):
            pass
        else:
            for d in data:
                if (d['reich']!= reich.pk):
                    d['count']= -1
                    d['leaders']= -1
                    d['mounts']= -1
                    d['lkp']= -1
                    d['skp']= -1
                    d['isGuard']= False
        returnData = json.dumps(data)
        return HttpResponse(returnData)

def getLastSavedTimeStamp(request):
    stamp = LastSavedTimeStamp.objects.all().first()
    time = json.dumps(str(stamp.timeStamp))
    return HttpResponse(time)

def buildingData(request):
    all_buildings_data = serializers.serialize('python', Ruestgueter.objects.all())
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
        currentMapData.filter(x = typeXY[1]).filter(y = typeXY[2]).delete()
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
    currentRiverData = Fluesse.objects.all()
    riverData = request.POST.get("river")
    listOfData = riverData.split(";")
    for listItem in listOfData:
        xyxy = listItem.split(",")
        currentRiverData.filter(firstX=xyxy[0]).filter(firstY=xyxy[1]).filter(secondX=xyxy[2]).filter(secondY=xyxy[3]).delete()
        river = Fluesse()
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
    currentBuildingData = Ruestgueter.objects.all()
    buildingData = request.POST.get("buildings")
    listOfData = buildingData.split(";")
    for listItem in listOfData:
        building = listItem.split(",")
        if int(building[0]) <= 4:
            currentBuildingData.filter(type=building[0]).filter(reich=building[1]).filter(x=building[2])\
                .filter(y=building[3]).delete()
            newBuilding = Ruestgueter()
            newBuilding.type = building[0]
            newBuilding.reich = Reich.objects.get(pk= building[1])
            newBuilding.x = building[2]
            newBuilding.y = building[3]
            newBuilding.save()
        elif int(building[0]) <= 7:
            currentBuildingData.filter(type=building[0]).filter(reich=building[1]).filter(x=building[2])\
                .filter(y=building[3]).filter(direction=building[4]).delete()
            newBuilding = Ruestgueter()
            newBuilding.type = building[0]
            newBuilding.reich = Reich.objects.get(pk= building[1])
            newBuilding.x = building[2]
            newBuilding.y = building[3]
            newBuilding.direction = building[4]
            newBuilding.save()
        elif int(building[0]) <= 8:
            currentBuildingData.filter(type=building[0]).filter(reich=building[1]).filter(firstX=building[2])\
                .filter(firstY=building[3]).filter(secondX=building[4]).filter(secondY=building[5]).delete()
            newBuilding = Ruestgueter()
            newBuilding.type = building[0]
            newBuilding.reich = Reich.objects.get(pk= building[1])
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
    if ((sessionKey == '0') | (sessionKey == None)):
        pass
    else:
        user = Token.objects.get(key=sessionKey).user
        reich = Reichszugehoerigkeit.objects.get(user=user).reich
        currentArmyData = Truppen.objects.all()
        armydata = request.POST.get("armies")
        listOfData = armydata.split(";")
        for listItem in listOfData:
            axyo = listItem.split(",") # Army axyo[0-5], X = axyo[6], Y = axyo[7], Owner = axyo[8]
            if(reich == Reich.objects.get(pk = axyo[8])):
                currentArmyData.filter(armyId = axyo[0]).filter(reich = Reich.objects.get(pk = axyo[8])).delete()
                army = Truppen()
                army.armyId = axyo[0]
                army.count = axyo[1]
                army.leaders = axyo[2]
                army.lkp = axyo[3]
                army.skp = axyo[4]
                army.mounts = axyo[5]
                army.x = axyo[6]
                army.y = axyo[7]
                army.reich = Reich.objects.get(pk= axyo[8])
                army.save()
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()
    return HttpResponse("done")

def saveBorderData(request):
    currentBorderData = Reichsgebiet.objects.all()
    borderdata = request.POST.get("borders")
    listOfData = borderdata.split(";")
    for listItem in listOfData:
        reichfieldlist = listItem.split(":")
        owner = Reich.objects.get(name = reichfieldlist[0])
        fields = reichfieldlist[1].split(",")
        for field in fields:
            xy = field.split("/")
            currentBorderData.filter(x = xy[0]).filter(y = xy[1]).delete()
            reichsgebiet = Reichsgebiet()
            reichsgebiet.reich = owner
            reichsgebiet.x = xy[0]
            reichsgebiet.y = xy[1]
            reichsgebiet.save()
    LastSavedTimeStamp.objects.all().delete()
    saveTime = LastSavedTimeStamp()
    saveTime.save()
    return HttpResponse("done")

def getBorderData(request):
    all_border_data = serializers.serialize('python', Reichsgebiet.objects.all())
    data = [d['fields'] for d in all_border_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)

def getRiverData(request):
    all_river_data = serializers.serialize('python', Fluesse.objects.all())
    data = [d['fields'] for d in all_river_data]
    returnData = json.dumps(data)
    return HttpResponse(returnData)

def getCSRFToken(request): ## funktioniert nicht
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

            user = form.save(commit = False)

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
            # Add the token to the return serialization
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'staff': user.is_staff
            }
            returnData = json.dumps(data)
            return HttpResponse(returnData)
        else:
            return HttpResponse('This account is not Active.')
    else:
        return HttpResponse('Username/password combination invalid.')