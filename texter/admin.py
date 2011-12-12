from django.contrib import admin
from . import models


class ExperimentAdmin(admin.ModelAdmin):

    readonly_fields = ['url_slug', ]


class BackendAdmin(admin.ModelAdmin):

    readonly_fields = ['delegate_classname', 'delegate_pk', 'name']

admin.site.register(models.Experiment, ExperimentAdmin)

admin.site.register(models.Backend, BackendAdmin)
