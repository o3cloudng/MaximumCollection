from django.shortcuts import render, redirect
from tax.forms import PermitForm, PermitEditForm, RemittanceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import User, AdminSetting
from tax.models import Permit, InfrastructureType, Waver
from datetime import date, datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django_htmx.http import HttpResponseClientRedirect
from django.db.models import Q, Count, Avg, Sum, Max
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.http import HttpResponse


@login_required
def undispute_demand_notice_receipt(request, ref_id):
    permits = Permit.objects.filter(referenceid = ref_id, is_disputed=True)
    if not permits.first().company == request.user:
        return redirect('apply_for_permit')
    
    ref = permits.first()
    app_fee = AdminSetting.objects.get(slug="application-fee")
    site_assessment = AdminSetting.objects.get(slug="site-assessment")
    admin_pm_fees = AdminSetting.objects.get(slug="admin-pm-fees")

    mast_roof = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=False), Q(infra_type__infra_name__istartswith='Mast') | Q(infra_type__infra_name__istartswith='Roof'))
    length = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=False), Q(infra_type__infra_name__istartswith='Optic') | Q(infra_type__infra_name__istartswith='Gas') | Q(infra_type__infra_name__istartswith='Power') | Q(infra_type__infra_name__istartswith='Pipeline'))
    #application number = number of masts and rooftops 

    mast_roof_no = mast_roof.aggregate(no_sites = Sum('amount'))
    
    app_count = mast_roof_no['no_sites'] + length.count()
    total_app_fee = app_count * app_fee.rate

    tot_sum_infra = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_disputed=True)).aggregate(no_sum = Sum('infra_cost'))
    # print("Tot Sum: ", tot_sum_infra)

    # Site assessment report rate
    sar_rate = mast_roof_no['no_sites'] * site_assessment.rate

    admin_pm_fees_sum = admin_pm_fees.rate * tot_sum_infra['no_sum'] / 100

    total_due = tot_sum_infra['no_sum'] + total_app_fee + admin_pm_fees_sum + sar_rate

    # ADD WAVER
    if Waver.objects.filter(referenceid=ref).exists():
        waver = Waver.objects.get(referenceid=ref).wave_amount
    else:
        waver = 0
    
    # print("WAVER: ", waver)
    total_liability = total_due - waver
    

    context = {
        'permits': permits,
        'ref': ref,
        'site_assessment': site_assessment,
        'site_assess_count': mast_roof_no['no_sites'],
        'admin_pm_fees': admin_pm_fees,
        'app_fee': app_fee,
        'app_count': app_count,
        'total_app_fee': total_app_fee,
        'sar_rate': sar_rate,
        'tot_sum_infra': tot_sum_infra,
        'admin_pm_fees_sum': admin_pm_fees_sum,
        'total_due': total_due,
        'waver': waver,
        'total_liability': total_liability,
        'ref_id': ref_id
    }
    return render(request, 'tax-payers/receipts/undisputed_dn_receipt.html', context)

@login_required
def add_dispute_dn_edit(request):
    ref_id = str(request.POST['referenceid'])
    # print("REF: ", ref_id)
    if request.htmx:
        form = PermitEditForm(request.POST or None, request.FILES or None)

        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])
        # print("READY POST: ", infra_rate.rate, type(infra_rate.rate))
        # print("Permit type: ", request.POST['amount'], type(request.POST['amount']))
        if "mast" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        elif "roof" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        else:
            infra_cost = infra_rate.rate * int(request.POST['length'])
            qty = 0
            len = request.POST['length']

        print("AMOUNT OR NUMBER: ", infra_rate.infra_name.lower())

        if form.is_valid():
            # print("Form is valid")
            permit = form.save(commit=False)
            permit.referenceid = ref_id
            permit.company = request.user
            permit.amount = qty
            permit.length = len
            permit.infra_cost = infra_cost
            permit.is_disputed = True
            permit.save()

            context = {
                'form':form,
                'referenceid': ref_id,
                'company': request.user
            }
            return HttpResponseClientRedirect('/tax/apply/permit/dispute_notice/'+permit.referenceid)

        else:
            print("FILE FORMAT INVALID")
    form = PermitForm()

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }
    return HttpResponseClientRedirect('/tax/apply/permit/dispute_notice/'+permit.referenceid)


@login_required
def add_undispute_edit(request):
    ref_id = request.POST['referenceid']
    if request.method == 'POST':
        form = PermitEditForm(request.POST or None, request.FILES or None)

        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])
        # print("READY POST: ", infra_rate.rate, type(infra_rate.rate))
        # print("Permit type: ", request.POST['amount'], type(request.POST['amount']))
        if "mast" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        elif "roof" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        else:
            infra_cost = infra_rate.rate * int(request.POST['length'])
            qty = 0
            len = request.POST['length']

        print("REFERENCE ID: ", ref_id)

        if form.is_valid():
            # print("Form is valid")
            permit = form.save(commit=False)
            permit.referenceid = ref_id
            permit.company = request.user
            permit.amount = qty
            permit.length = len
            permit.infra_cost = infra_cost
            permit.is_disputed = True
            permit.save()

            context = {
                'form':form,
                'referenceid': ref_id,
                'company': request.user
            }
            return HttpResponseClientRedirect('/tax/apply/permit/dispute_notice/'+permit.referenceid)

        else:
            print("FILE FORMAT INVALID")
    form = PermitForm()

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }
    return HttpResponseClientRedirect('/tax/apply/permit/dispute_notice/'+permit.referenceid)


@login_required
def add_ex_undispute_edit(request):
    ref_id = request.POST['referenceid']
    if request.method == 'POST':
        form = PermitEditForm(request.POST or None, request.FILES or None)

        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])
        # print("READY POST: ", infra_rate.rate, type(infra_rate.rate))
        # print("Permit type: ", request.POST['amount'], type(request.POST['amount']))
        if "mast" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        elif "roof" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        else:
            infra_cost = infra_rate.rate * int(request.POST['length'])
            qty = 0
            len = request.POST['length']

        print("REFERENCE ID: ", ref_id)

        if form.is_valid():
            # print("Form is valid")
            permit = form.save(commit=False)
            permit.referenceid = ref_id
            permit.company = request.user
            permit.amount = qty
            permit.length = len
            permit.infra_cost = infra_cost
            permit.is_disputed = True
            permit.is_existing = True
            permit.save()

            context = {
                'form':form,
                'referenceid': ref_id,
                'company': request.user
            }
            return HttpResponseClientRedirect('/tax/apply/permit/dispute_ex_notice/'+permit.referenceid)

        else:
            print("FILE FORMAT INVALID")
    form = PermitForm()

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }
    return HttpResponseClientRedirect('/tax/apply/permit/dispute_notice/'+permit.referenceid)


@login_required
def del_undisputed_edit(request, pk):
    permit = Permit.objects.get(pk=pk)
    permit.delete()

    return HttpResponseClientRedirect('/tax/apply/permit/dispute_notice/'+permit.referenceid)

@login_required
def del_ex_undisputed_edit(request, pk):
    permit = Permit.objects.get(pk=pk)
    permit.delete()

    return HttpResponseClientRedirect('/tax/apply/permit/dispute_ex_notice/'+permit.referenceid)


@login_required
def accept_undisputed_edit(request, pk):
    permit = Permit.objects.get(pk=pk)
    print("DATE FORMAT: ", date.today(), type(str(date.today())))
    # yr = datetime.strptime(str(permit.year_installed), "%m/ %d/%Y %H:%M:%S")
    # print(yr)
    data = {
        'company': permit.company,
        'referenceid': permit.referenceid,
        'infra_type': permit.infra_type,
        'amount': permit.amount,
        'length': permit.length,
        'add_from': permit.add_from,
        'add_to': permit.add_to,
        'year_installed': str(date.today()),
        'age': permit.age,
        'upload_application_letter': permit.upload_application_letter,
        'upload_asBuilt_drawing': permit.upload_asBuilt_drawing,
        'upload_payment_receipt': permit.upload_payment_receipt,
        'status': permit.status,
        'is_disputed': True,
        'is_undisputed': permit.is_undisputed,
        'is_revised': permit.is_revised,
        'is_paid': permit.is_paid,
        'is_existing': permit.is_existing
    }
    disputed_permit = Permit(data)
    disputed_permit.save()

    return HttpResponseClientRedirect('/tax/apply/permit/dispute_notice/'+permit.referenceid)

@login_required
def dispute_dn_edit(request, pk):
    permit = Permit.objects.get(pk=pk)
    form = PermitEditForm(instance = permit)
    context = {
        'form': form
    }
    return render(request, 'tax-payers/partials/apply_permit_edit_form.html', context)

@login_required
def dispute_demand_notice(request, ref_id):

    ref = Q(referenceid=ref_id)
    coy = Q(company=request.user)
    is_dis = Q(is_disputed = False)
    not_dis = Q(is_disputed = True)
    permits = Permit.objects.filter(ref & coy & is_dis)
    undisputed_permits = Permit.objects.filter(ref & coy & not_dis)
    # print("PERMIT COUNT: ", permits)
    # print("UNDISPUTED COUNT: ", undisputed_permits)
    
    # if request.method == "POST":
    #     print("POST SHOWS HERE....")
   
    context = {
        'ref_id': ref_id,
        'permits': permits,
        'undisputed_permits': undisputed_permits
    }
    return render(request, 'tax-payers/apply_for_permit_edit.html', context)

def generate_ref_id():
    today = date.today()
    year = str(today.year)
    month = str(today.month).zfill(2)
    return year+month

@login_required
def apply_for_permit(request):
    if Permit.objects.all().exists(): 
        last = Permit.objects.latest("pk").id
        ref_id = "LA"+generate_ref_id() + str(last + 1).zfill(5)
    else:
        ref_id = generate_ref_id() + "00001"

    print("NEW: APPLY FOR NEW PERMIT")

    if request.method == 'POST':
        form = PermitForm(request.POST or None, request.FILES or None)

        # Get the rate for each infrastructure from the InfrastructureType Table
        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])
        # print("READY POST: ", infra_rate.rate, type(infra_rate.rate))
        # print("Permit type: ", request.POST['amount'], type(request.POST['amount']))

        # If Infrastructure is a Mast or Roof - Make length = 0 and infra_cost = rate * quantity
        # If Infrastructure is a others - Make amount = 0 and infra_cost = the rate * length
        if "mast" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        elif "roof" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        else:
            infra_cost = infra_rate.rate * int(request.POST['length'])
            qty = 0
            len = request.POST['length']

        # print("REFERENCES: ", request.POST)

        if form.is_valid():
            # print("Form is valid")
            permit = form.save(commit=False)
            permit.referenceid = request.POST['reference']
            permit.company = request.user
            permit.amount = qty
            permit.length = len
            permit.infra_cost = infra_cost
            permit.save()
        else:
            print(form.errors)
    form = PermitForm()

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }

    # print("APPLY PERMIT - CONTEXT: ", context)

    if request.htmx:
        messages.success(request,"Infrastructure added successfully.")
        return HttpResponseClientRedirect('/tax/apply/permit/demand_notice/'+permit.referenceid)

    return render(request, 'tax-payers/apply_for_permit.html', context)

@login_required
def apply_for_permit_edit(request, ref_id):

    permits = Permit.objects.filter(referenceid = ref_id)
    infra_type = InfrastructureType.objects.all()

    if request.htmx:
        form = PermitForm(request.POST or None, request.FILES or None)
        infra = InfrastructureType.objects.get(id=request.POST['infra_type'])
        print("INFRA: ", infra)
        form.infra_type = infra

        # Get the rate for each infrastructure from the InfrastructureType Table
        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])

        # If Infrastructure is a Mast or Roof - Make length = 0 and infra_cost = the rate * quantity
        # If Infrastructure is a  - Make length = 0 and infra_cost = the rate * length
        if "mast" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        elif "roof" in infra_rate.infra_name.lower():
            infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        else:
            infra_cost = infra_rate.rate * int(request.POST['length'])
            qty = 0
            len = request.POST['length']

        if form.is_valid():
            print("Dispute Form is valid")
            permit = form.save(commit=False)
            permit.referenceid = ref_id
            permit.company = request.user
            permit.amount = qty
            permit.length = len
            permit.infra_cost = infra_cost
            permit.save()
        else:
            print(form.errors)
        

    # form = PermitForm(instance = permits)
    context = {
        'permits': permits,
        'ref_id': ref_id,
        'infra_type': infra_type,
        'form': form
    }
    print("APPLY PERMIT EDIT CONTEXT: ", context)
    if request.htmx:
        messages.success(request,"Infrastructure disputed successfully.")
        return HttpResponseClientRedirect('/tax/apply/permit/edit/'+ref_id)
    
    return render(request, 'tax-payers/apply_for_permit_edit.html', context)


@login_required # Check this after
def add_permit_form(request):
    if Permit.objects.all().exists(): 
        last = Permit.objects.latest("pk").id
        ref_id = "LA"+generate_ref_id() + str(last + 1).zfill(5)
    else:
        ref_id = generate_ref_id() + "00001"
    
    permits = Permit.objects.all()
    if request.method == "POST":
        form = PermitForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            permit = form.save(commit=False)
            # permit.referenceid = ref_id
            permit.referenceid = request.user
            permit.save()
            permits = Permit.objects.all()
            context = {
                'permits': permits
            }

            print("USER ID: ", permits)
            return render(request, 'tax-payers/partials/permit_details.html', context)
        else:
            print("ERROR: ", form.errors)

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }
    return render(request, 'tax-payers/partials/apply_permit_form.html', context)


@login_required 
def add_new_permit_form(request, ref_id):
    
    permits = Permit.objects.all()
    if request.method == "POST":
        form = PermitForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            permit = form.save(commit=False)
            # permit.referenceid = ref_id
            permit.referenceid = request.POST['referenceid']
            permit.is_disputed = True
            permit.save()
            permits = Permit.objects.all()
            context = {
                'permits': permits
            }

            return render(request, 'tax-payers/partials/permit_details.html', context)
        else:
            print(form.errors)

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }
    return render(request, 'tax-payers/partials/apply_new_permit_form.html', context)


@login_required 
def add_new_ex_permit_form(request, ref_id):
    
    permits = Permit.objects.all()
    if request.method == "POST":
        form = PermitForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            permit = form.save(commit=False)
            # permit.referenceid = ref_id
            permit.referenceid = request.POST['referenceid']
            permit.is_disputed = True
            # permit.is_existing = True
            permit.save()
            permits = Permit.objects.all()
            context = {
                'permits': permits
            }

            return render(request, 'tax-payers/partials/permit_details.html', context)
        else:
            print(form.errors)

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }
    return render(request, 'tax-payers/partials/apply_new_ex_permit_form.html', context)


# @login_required
# def existing_permit(request):
#     if Permit.objects.all().exists(): 
#         last = Permit.objects.latest("pk").id
#         ref_id = "LA"+generate_ref_id() + str(last + 1).zfill(5)
#     else:
#         ref_id = generate_ref_id() + "00001"

#     if request.htmx:
#         print("EXISTING PERMIT - REF: ", ref_id)
#         form = PermitForm(request.POST or None, request.FILES or None)

#         print("READY POST")

#         if form.is_valid():
#             print("Form is valid")
#             permit = form.save(commit=False)
#             permit.referenceid = ref_id
#             permit.company = request.user
#             permit.save()
#         else:
#             print("FILE FORMAT INVALID")
#     form = PermitForm()

#     context = {
#         'form':form,
#         'referenceid': ref_id,
#         'company': request.user
#     }

#     if request.htmx:
#         return HttpResponseClientRedirect('/tax/apply/permit/payment_receipt/'+permit.referenceid)

#     return render(request, 'tax-payers/apply_for_permit.html', context)

@login_required
def resources(request):
    context = {}
    return render(request, 'tax-payers/resources.html', context)

@login_required
def upload_existing_facilities(request):
    context = {}
    return render(request, 'tax-payers/upload-existing-facility.html', context)

@login_required
def demand_notice_receipt(request, ref_id):
    permits = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=False))
    if not permits.exists():
        return redirect('apply_for_permit')
    
    if not permits.first().company == request.user:
        return redirect('apply_for_permit')
    
    ref = permits.first()
    app_fee = AdminSetting.objects.get(slug="application-fee")
    site_assessment = AdminSetting.objects.get(slug="site-assessment")
    admin_pm_fees = AdminSetting.objects.get(slug="admin-pm-fees")

    mast_roof = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=False), Q(infra_type__infra_name__istartswith='Mast') | Q(infra_type__infra_name__istartswith='Roof'))
    length = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=False), Q(infra_type__infra_name__istartswith='Optic') | Q(infra_type__infra_name__istartswith='Gas') | Q(infra_type__infra_name__istartswith='Power') | Q(infra_type__infra_name__istartswith='Pipeline'))
    #application number = number of masts and rooftops 

    mast_roof_no = mast_roof.aggregate(no_sites = Sum('amount'))
    
    app_count = mast_roof_no['no_sites'] + length.count()
    total_app_fee = app_count * app_fee.rate

    tot_sum_infra = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_disputed=False)).aggregate(no_sum = Sum('infra_cost'))
    print("tot_sum_infra: ", Permit.objects.filter(Q(referenceid = ref_id)))
    # Site assessment report rate
    sar_rate = mast_roof_no['no_sites'] * site_assessment.rate

    admin_pm_fees_sum = admin_pm_fees.rate * tot_sum_infra['no_sum'] / 100

    total_due = tot_sum_infra['no_sum'] + total_app_fee + admin_pm_fees_sum + sar_rate

    # ADD WAVER
    if Waver.objects.filter(referenceid=ref).exists():
        waver = Waver.objects.get(referenceid=ref).wave_amount
    else:
        waver = 0
    
    # print("WAVER: ", waver)
    total_liability = total_due - waver
    

    context = {
        'permits': permits,
        'ref': ref,
        'site_assessment': site_assessment,
        'site_assess_count': mast_roof_no['no_sites'],
        'admin_pm_fees': admin_pm_fees,
        'app_fee': app_fee,
        'app_count': app_count,
        'total_app_fee': total_app_fee,
        'sar_rate': sar_rate,
        'tot_sum_infra': tot_sum_infra,
        'admin_pm_fees_sum': admin_pm_fees_sum,
        'total_due': total_due,
        'waver': waver,
        'total_liability': total_liability,
        'ref_id': ref_id
    }
    return render(request, 'tax-payers/receipts/demand-notice-receipt.html', context)

@login_required
def dispute_demand_notice_receipt(request, ref_id):
    print("DN - REF ID: ", ref_id)
    permits = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=True))
    if not permits.first().company == request.user:
        return redirect('dashboard')
    
    ref = permits.first()
    app_fee = AdminSetting.objects.get(slug="application-fee")
    site_assessment = AdminSetting.objects.get(slug="site-assessment")
    admin_pm_fees = AdminSetting.objects.get(slug="admin-pm-fees")

    mast_roof = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=True), Q(infra_type__infra_name__istartswith='Mast') | Q(infra_type__infra_name__istartswith='Roof'))
    length = Permit.objects.filter(Q(referenceid = ref_id, is_disputed=True), Q(infra_type__infra_name__istartswith='Optic') | Q(infra_type__infra_name__istartswith='Gas') | Q(infra_type__infra_name__istartswith='Power') | Q(infra_type__infra_name__istartswith='Pipeline'))
    #application number = number of masts and rooftops 

    mast_roof_no = mast_roof.aggregate(no_sites = Sum('amount'))
    
    app_count = mast_roof_no['no_sites'] + length.count()
    total_app_fee = app_count * app_fee.rate

    tot_sum_infra = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_disputed=True)).aggregate(no_sum = Sum('infra_cost'))
    # print(Permit.objects.filter(Q(referenceid = ref_id, is_disputed=True)))
    # Site assessment report rate
    sar_rate = mast_roof_no['no_sites'] * site_assessment.rate

    admin_pm_fees_sum = admin_pm_fees.rate * tot_sum_infra['no_sum'] / 100

    total_due = tot_sum_infra['no_sum'] + total_app_fee + admin_pm_fees_sum + sar_rate

    # ADD WAVER
    if Waver.objects.filter(referenceid=ref).exists():
        waver = Waver.objects.get(referenceid=ref).wave_amount
    else:
        waver = 0
    
    # print("WAVER: ", waver)
    total_liability = total_due - waver
    

    context = {
        'permits': permits,
        'ref': ref,
        'site_assessment': site_assessment,
        'site_assess_count': mast_roof_no['no_sites'],
        'admin_pm_fees': admin_pm_fees,
        'app_fee': app_fee,
        'app_count': app_count,
        'total_app_fee': total_app_fee,
        'sar_rate': sar_rate,
        'tot_sum_infra': tot_sum_infra,
        'admin_pm_fees_sum': admin_pm_fees_sum,
        'total_due': total_due,
        'waver': waver,
        'total_liability': total_liability,
        'ref_id': ref_id,
        'is_disputed': True
    }
    return render(request, 'tax-payers/receipts/undisputed-receipt.html', context)

