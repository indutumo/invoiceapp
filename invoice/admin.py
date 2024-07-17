from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Organization)
class OrganizationAdmin(ImportExportModelAdmin):
    list_display = ('name','mobile_number','email_address')
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin):
    list_display = ('client','mobile_number','email_address','total')
    list_filter = ['client']
    search_fields = ['client']