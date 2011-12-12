from django.contrib import admin
from . import models


class TropoBackendAdmin(admin.ModelAdmin):

    readonly_fields = ['qualified_classname']

admin.site.register(models.TropoBackend, TropoBackendAdmin)
