from django.contrib import admin
from django.utils.html import format_html

import datetime

from .models import Instrument
from .models import Place
from .models import Category, Manufacturer, User
# Register your models here.


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('eql', 'sn', 'model', 'calibration_date', 'calibration_due',
                    'pm_date', 'pm_due', 'release_date', 'status',
                    'retire_date', 'place', 'primary_assignee', 'secondary_assignee', 'note', 'is_overdue')
    list_filter = ('status', 'place', 'calibration_date',)
    search_fields = ('eql', 'sn')
    
    def is_overdue(self, obj):
        nowdate = datetime.datetime.date(datetime.datetime.now())
        distance = obj.calibration_due - nowdate
        if distance.days < 0:
            return format_html(
                '<span style="color: red;">{}</span>',
                (f'已超期{abs(distance.days)}天')
            )
        elif distance.days >= 0:
            return format_html(
                '<span style="color: black;">{}</span>',
                (f'{abs(distance.days)}天')
            )
        else:
            return format_html(
                '<span style="color: black;">{}</span>',
                ('ERROR')
            )
    is_overdue.admin_order_field = 'calibration_due'
    is_overdue.short_description = '距离到期'


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
