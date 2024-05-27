from django.urls import path
from tax.views import *

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('apply/permit/', apply_for_permit, name="apply_for_permit"),
    path('apply/permit/add_permit_form/', add_permit_form, name="add_permit_form"),
    path('apply/permit/upload_existing_facilities/', upload_existing_facilities, name="upload-existing-facilities"),
    path('apply/permit/demand_notice/', demand_notice, name="demand-notice"),
    path('apply/permit/disputes/', disputes, name="disputes"),
    path('apply/permit/infrastructures/', infrastructures, name="infrastructures"),
    path('apply/permit/downloads/', downloads, name="downloads"),
    path('apply/permit/admin_settings/', admin_settings, name="admin-settings"),
    path('apply/permit/payment_receipt/<str:ref_id>/', payment_receipt, name="payment-receipt"),
    path('apply/permit/resources/', resources, name="resources"),
    path('template/', template, name="template"),
]
