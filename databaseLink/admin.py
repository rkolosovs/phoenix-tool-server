from django.contrib import admin
from .models import Reich, Event, Reichszugehoerigkeit, Char, Ruestgueter, Field, Reichsgebiet, Fluesse, Zugreihenfolge, Truppen

admin.site.register(Reich)
admin.site.register(Reichszugehoerigkeit)
admin.site.register(Char)
admin.site.register(Ruestgueter)
admin.site.register(Field)
admin.site.register(Fluesse)
admin.site.register(Zugreihenfolge)
admin.site.register(Truppen)
admin.site.register(Reichsgebiet)
admin.site.register(Event)