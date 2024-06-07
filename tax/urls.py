from django.urls import path
from tax.views import *

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('apply/permit/', apply_for_permit, name="apply_for_permit"),
    path('apply/permit/existing_permit', existing_permit, name="existing_permit"),
    path('apply/permit/add_permit_form/', add_permit_form, name="add_permit_form"),
    path('apply/permit/edit/<str:ref_id>/', apply_for_permit_edit, name="apply_for_permit_edit"),
    path('apply/permit/upload_existing_facilities/', upload_existing_facilities, name="upload-existing-facilities"),
    path('apply/permit/demand_notice/', demand_notice, name="demand-notice"),
    path('apply/permit/disputes/', disputes, name="disputes"),
    path('apply/permit/infrastructures/', infrastructures, name="infrastructures"),
    path('apply/permit/downloads/', downloads, name="downloads"),
    path('apply/permit/settings/', settings, name="settings"),
    path('apply/permit/demand_notice/<str:ref_id>/', payment_receipt, name="payment-receipt"),
    path('apply/permit/dispute_notice/<str:ref_id>/', dispute_demand_notice, name="dispute-demand-notice"),
    path('apply/permit/demand_notice/receipt/<str:ref_id>/', dispute_demand_notice_receipt, name="dispute-demand-notice-receipt"),
    path('apply/permit/resources/', resources, name="resources"),
    # path('template/', template, name="template"),
]
