from django.contrib import admin

from repairs.models import (
    Parts, PlacesWork, Repair, TypesRepair, Locomotive, Work,
)

admin.site.register(Parts)
admin.site.register(Work)
admin.site.register(PlacesWork)
admin.site.register(TypesRepair)
admin.site.register(Locomotive)
admin.site.register(Repair)
