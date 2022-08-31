# Django
from django.contrib.gis import admin

# Models
from warrants.models import Warrant


class WarrantAdmin(admin.GISModelAdmin):
    pass


admin.site.register(Warrant, WarrantAdmin)
