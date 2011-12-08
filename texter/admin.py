from django.contrib import admin
from . import models

class ExperimentAdmin(admin.ModelAdmin):
    
    readonly_fields = ['url_slug', ]

admin.site.register(models.Experiment, ExperimentAdmin)
