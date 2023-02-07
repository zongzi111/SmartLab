from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse

import datetime

from .models import Instrument
from .models import Place
from .models import Category, Manufacturer, User
import xlwt
# Register your models here.

def export_selected_objects_to_excel(self, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="selected_objects.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('objects')
    row_num = 0
    columns = [field.name for field in self.model._meta.fields]

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    for obj in queryset:
        row_num += 1
        row = []
        for field in columns:
            field_obj = self.model._meta.get_field(field)
            if field_obj.choices:
                value = getattr(obj, "get_%s_display" % field)()
            else:
                value = getattr(obj, field)
            row.append(value)
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value))
    wb.save(response)
    return response

export_selected_objects_to_excel.short_description = "导出为excel"

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('eql', 'sn', 'model', 'calibration_date', 'calibration_due',
                    'pm_date', 'pm_due', 'release_date', 'status',
                    'retire_date', 'place', 'primary_assignee', 'secondary_assignee', 'note', 'is_overdue')
    list_filter = ('status', 'place', 'calibration_date',)
    search_fields = ('eql', 'sn')
    empty_value_display = 'NA'

    def is_overdue(self, obj):
        nowdate = datetime.datetime.date(datetime.datetime.now())
        
        if obj.calibration_due:
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
                ('NA')
            )
    is_overdue.admin_order_field = 'calibration_due'
    is_overdue.short_description = '距离到期'

    actions = [export_selected_objects_to_excel]


admin.site.register(Instrument, InstrumentAdmin)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('room_name',)


admin.site.register(Place, PlaceAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_zh', 'name_en', 'model', 'classification', 'Range')


admin.site.register(Category, CategoryAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)

    actions = [export_selected_objects_to_excel]

admin.site.register(Manufacturer, ManufacturerAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(User,  UserAdmin)
