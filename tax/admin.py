from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from tax.models import Permit, InfrastructureType, Waver, Remittance

# admin.site.register(Permit)
admin.site.register(InfrastructureType)
admin.site.register(Waver)
admin.site.register(Remittance)


@admin.register(Permit)
class PermitAdmin(ImportExportModelAdmin):
    list_display = ['referenceid', 'company', 'infra_type', 'amount', 'length', 'is_disputed', 'is_existing', 'year_installed']