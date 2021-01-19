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
    list_display = ('mediator', 'directory_path')
    search_fields = ['mediator',]

admin.site.register(Mediator, MediatorAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(FilePath, FilePathAdmin)


admin.site.site_header = 'File Sync Panel'
admin.site.site_url = '/dashboard'
admin.site.site_title = 'File Sync Panel'
admin.site.index_title = 'App Configurations'