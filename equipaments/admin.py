from django.contrib import admin

from equipaments.models import Equipament


class EquipamentAdmin(admin.ModelAdmin):
    list_display = ("code", "vessel", "status")
    list_filter = ["status"]
    search_fields = ["code", "vessel"]


admin.site.register(Equipament, EquipamentAdmin)
