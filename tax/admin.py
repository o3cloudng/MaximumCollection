from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from tax.models import Permit, InfrastructureType, Waver

# admin.site.register(Permit)
admin.site.register(InfrastructureType)
admin.site.register(Waver)


@admin.register(Permit)
class PermitAdmin(ImportExportModelAdmin):
    list_display = ['referenceid', 'company', 'infra_type', 'amount', 'length', 'year_installed', 'is_existing']