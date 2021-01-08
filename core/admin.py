from django.contrib import admin
from core.models import Mediator, File, FilePath

# Register your models here.
class MediatorAdmin(admin.ModelAdmin):
    list_display = ('mediator_name', 'details','is_active')
    search_fields = ['mediator_name',]

class FileAdmin(admin.ModelAdmin):
    list_display = ('mediator', 'file_name','end_point')
    search_fields = ['mediator',]


class FilePathAdmin(admin.ModelAdmin):
    list_display = ('mediator', 'file_path', 'path_type')
    search_fields = ['mediator',]

admin.site.register(Mediator, MediatorAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(FilePath, FilePathAdmin)