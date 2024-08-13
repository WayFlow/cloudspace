from django.contrib import admin

from .models import *

class CompanyAdminView(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'created_by')
class ProjectAdminView(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'company')

admin.site.register(Company, CompanyAdminView)
admin.site.register(Project, ProjectAdminView)