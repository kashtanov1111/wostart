from django.contrib import admin

from .models import Startup, StartupImage

class PropertyImageInline(admin.TabularInline):
    model = StartupImage
    extra = 1

class StartupAdmin(admin.ModelAdmin):
    inlines = [ PropertyImageInline, ]

admin.site.register(Startup, StartupAdmin)
admin.site.register(StartupImage)