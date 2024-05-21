from django.urls import path
from tax.views import apply_for_permit, demand_notice, add_permit_form, template, dashboard, disputes

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('apply/permit/', apply_for_permit, name="apply_for_permit"),
    path('apply/permit/demand_notice/', demand_notice, name="demand-notice"),
    path('apply/permit/disputes/', disputes, name="disputes"),
    path('apply/permit/add_permit_form/', add_permit_form, name="add_permit_form"),
    path('template/', template, name="template"),
]
