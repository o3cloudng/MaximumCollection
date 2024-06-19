from django.urls import path
from .views import view, view_existing_infrastructure, page_view

urlpatterns = [
    path('apply/permit/', view.apply_for_permit, name="apply_for_permit"),
    path('apply/permit/edit/<str:ref_id>/', view.apply_for_permit_edit, name="apply_for_permit_edit"),
    path('apply/permit/demand_notice/<str:ref_id>/', view.demand_notice_receipt, name="demand-notice-receipt"),
    path('apply/permit/dispute_notice/<str:ref_id>/', view.dispute_demand_notice, name="dispute-demand-notice"),
    path('apply/permit/demand_notice/receipt/<str:ref_id>/', view.dispute_demand_notice_receipt, name="dispute-demand-notice-receipt"),
    path('apply/permit/undisputed_notice_receipt/<str:ref_id>/', view.undispute_demand_notice_receipt, name="undispute_demand_notice_receipt"),
    path('apply/permit/resources/', view.resources, name="resources"),
    path('apply/permit/dn/edit/<int:pk>/', view.dispute_dn_edit, name="dispute-dn-edit"),
    path('apply/permit/dn/edit/add/', view.add_dispute_dn_edit, name="add_dispute_dn_edit"),
    path('apply/permit/add/', view.add_permit_form, name="add_permit_form"),
    # path('template/', template, name="template"),
    ####### Exisiting Infrastructures
    # path('apply/permit/existing_permit', view.existing_permit, name="existing_permit"),
    path('apply/permit/exist/', view_existing_infrastructure.apply_for_existing_permit, name="apply_existing_infra"),
    path('apply/permit/add_permit_ex_form/', view_existing_infrastructure.add_permit_ex_form, name="add_permit_ex_form"),
    path('apply/permit/demand_notice_ex/receipt/<str:ref_id>/', view_existing_infrastructure.demand_notice_ex_receipt, name="demand_notice_ex_receipt"),
    path('apply/permit/upload_existing_facilities/', view.upload_existing_facilities, name="upload-existing-facilities"),
    path('apply/permit/dispute_ex_notice/<str:ref_id>/', view_existing_infrastructure.dispute_ex_demand_notice, name="dispute-ex-demand-notice"),
    path('apply/permit/undisputed_ex_notice_receipt/<str:ref_id>/', view_existing_infrastructure.undispute_ex_demand_notice_receipt, name="undispute_ex_demand_notice_receipt"),
    path('apply/permit/ex/dn/edit/add/', view_existing_infrastructure.add_dispute_ex_dn_edit, name="add_ex_dispute_dn_edit"),
    path('apply/permit/ex/dn/edit/<int:pk>/', view_existing_infrastructure.dispute_ex_dn_edit, name="dispute_ex_dn_edit"),
    path('apply/waver', view_existing_infrastructure.apply_for_waver, name="apply_for_waver"),

    #  PAGES URL
    path('dashboard/', page_view.dashboard, name="dashboard"),
    path('demand_notice/', page_view.demand_notice, name="demand-notice"),
    path('disputes/', page_view.disputes, name="disputes"),
    path('infrastructures/', page_view.infrastructures, name="infrastructures"),
    path('downloads/', page_view.downloads, name="downloads"),
    path('settings/', page_view.settings, name="settings"),
]
