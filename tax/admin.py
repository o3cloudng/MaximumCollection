from django.contrib import admin
from tax.models import Permit, InfrastructureType, Waver

admin.site.register(Permit)
admin.site.register(InfrastructureType)
admin.site.register(Waver)


