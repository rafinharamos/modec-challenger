from django.contrib import admin

from vessels.models import Vessel


class VesselAdmin(admin.ModelAdmin):
    list_display = ("code",)
    search_fields = [
        "code",
    ]


admin.site.register(Vessel, VesselAdmin)
