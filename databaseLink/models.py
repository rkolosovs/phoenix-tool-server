from django.db import models

class Reich(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name + ' ' + str(self.pk)

class User(models.Model):
    firstName = models.CharField(max_length=250)
    secondName = models.CharField(max_length=250)

    def __str__(self):
        return self.firstName + ' ' +self.secondName

class Reichszugehoerigkeit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reich = models.ForeignKey(Reich, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ', ' + str(self.reich)

class Char(models.Model):
    charName = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.charName

class Ruestgueter(models.Model):
    DIRECTIONS = (
        ("nw", "north-west"),
        ("ne", "north-east"),
        ("e", "east"),
        ("se", "south-east"),
        ("sw", "south-west"),
        ("w", "west"),
    )
    reich = models.ForeignKey(Reich, on_delete=models.CASCADE)
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
        return str(self.reich) + ' ' + str(self.name) + ' ' + str(self.type) + ' ' + str(self.x) + ' ' + str(self.y) +\
               ' ' + str(self.direction) + ' ' + str(self.firstX) + ' ' + str(self.firstY) + ' ' + str(self.secondX)+\
               ' ' + str(self.secondY)

class Field(models.Model):
    type = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)

class Reichsgebiet(models.Model):
    reich = models.ForeignKey(Reich, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return str(self.reich) + ', ' + str(self.x) + ', ' + str(self.y)

class Fluesse(models.Model):
    firstX = models.IntegerField()
    firstY = models.IntegerField()
    secondX = models.IntegerField()
    secondY = models.IntegerField()

class Zugreihenfolge(models.Model):
    zugNummer = models.IntegerField()
    reihenfolge = models.IntegerField()
    subZug = models.IntegerField()

class Truppen(models.Model):
    reich = models.ForeignKey(Reich, on_delete=models.CASCADE)
    armyId = models.IntegerField()
    count = models.IntegerField()
    leaders = models.IntegerField()
    mounts = models.IntegerField()
    lkp = models.IntegerField()
    skp = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return str(self.reich) + ', ' + str(self.armyId)
