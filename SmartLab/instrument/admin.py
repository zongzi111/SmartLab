from django.contrib import admin

from .models import Instrument
from .models import Place
from .models import Category, Manufacturer, User
# Register your models here.


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('eql', 'sn', 'model', 'calibration_date', 'calibration_due',
                    'pm_date', 'pm_due', 'release_date', 'status',
                    'retire_date', 'place', 'primary_assignee', 'secondary_assignee', 'note')
    list_filter = ('status', 'place')
    search_fields = ('eql', 'sn')


admin.site.register(Instrument, InstrumentAdmin)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('room_name',)


admin.site.register(Place, PlaceAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_zh', 'name_en', 'model', 'classification', 'Range')


admin.site.register(Category, CategoryAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Manufacturer, ManufacturerAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(User,  UserAdmin)
