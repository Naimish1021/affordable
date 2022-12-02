from django.contrib import admin
from .models import Blog
from import_export.admin import ImportExportModelAdmin

from import_export import resources

class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog
class BlogAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = BlogResource
    list_display = ['name','city','state']
    search_fields = ['id','slug']
    list_filter = ['city']


admin.site.register(Blog,BlogAdmin)
