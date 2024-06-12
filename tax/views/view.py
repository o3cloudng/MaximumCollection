from django.shortcuts import render, redirect
from tax.forms import PermitForm, PermitEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import User, AdminSetting
from tax.models import Permit, InfrastructureType, Waver
from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django_htmx.http import HttpResponseClientRedirect
from django.db.models import Q, Count, Avg, Sum
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

    tot_sum_infra = Permit.objects.filter(referenceid = ref_id).aggregate(no_sum = Sum('infra_cost'))

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
    print("PERMIT COUNT: ", permits)
    print("UNDISPUTED COUNT: ", undisputed_permits)
    
    if request.method == "POST":
        print("POST SHOWS HERE....")
   
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

    print("WE RAE HERE...")

    if request.method == 'POST':
        print("REF: ", ref_id)
        form = PermitForm(request.POST or None, request.FILES or None)

        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])
        print("READY POST: ", infra_rate.rate, type(infra_rate.rate))
        print("Permit type: ", request.POST['amount'], type(request.POST['amount']))
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
            print("Form is valid")
            permit = form.save(commit=False)
            permit.referenceid = ref_id
            permit.company = request.user
            permit.amount = qty
            permit.length = len
            permit.infra_cost = infra_cost
            permit.save()
        else:
            print("FILE FORMAT INVALID")
    form = PermitForm()

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }

    if request.htmx:
        return HttpResponseClientRedirect('/tax/apply/permit/demand_notice/'+permit.referenceid)

    return render(request, 'tax-payers/apply_for_permit.html', context)

@login_required
def apply_for_permit_edit(request, ref_id):

    permits = Permit.objects.filter(referenceid = ref_id)
    infra_type = InfrastructureType.objects.all()
    # form = PermitForm(instance = permits)
    print("WE ARE HERE....")

    if request.htmx:
        form = PermitForm(request.POST or None, request.FILES or None)
        infra = InfrastructureType.objects.get(id=request.POST['infra_type'])
        print("INFRA: ", infra)
        form.infra_type = infra

        if form.is_valid():
            print("Form is valid")
            # permit = form.save(commit=False)
            # permit.infra_type = infra
            form.save()
        else:
            print(form.errors)
        

    # form = PermitForm(instance = permits)
    context = {
        'permits': permits,
        'ref_id': ref_id,
        'infra_type': infra_type,
        'form': form
    }
    if request.htmx:
        return HttpResponseClientRedirect('/tax/apply/permit/edit/'+ref_id)
    
    return render(request, 'tax-payers/apply_for_permit_edit.html', context)


@login_required
def add_permit_form(request):
    
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
        # 'referenceid': ref_id,
        'company': request.user
    }
    return render(request, 'tax-payers/partials/apply_permit_form.html', context)

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
def dashboard(request):
    user = User.objects.get(id = request.user.id)
    if user.is_profile_complete:
        context = {
            "is_profile_complete" : True,
            "user":user
        }

    demand_notices = Permit.objects.filter(company=request.user)
    demand_notices_paid = Permit.objects.filter(company=request.user, status="PAID")
    demand_notices_unpaid = Permit.objects.filter(company=request.user, status="UNPAID")
    demand_notices_disputed = Permit.objects.filter(company=request.user, status="DISPUTED")
    demand_notices_resolved = Permit.objects.filter(company=request.user, status="RESOLVED")
    context = {
         "is_profile_complete" : False,
         "demand_notices": demand_notices,
         "demand_notices_paid": demand_notices_paid,
         "demand_notices_unpaid": demand_notices_unpaid,
        "demand_notices_disputed": demand_notices_disputed,
        "demand_notices_resolved": demand_notices_resolved
    }
    return render(request, 'tax-payers/dashboard.html', context)


@login_required
def demand_notice(request):
    demand_notices = Permit.objects.filter(company=request.user)
    demand_notices_paid = Permit.objects.filter(company=request.user, status="PAID")
    demand_notices_unpaid = Permit.objects.filter(company=request.user, status="UNPAID")
    demand_notices_disputed = Permit.objects.filter(company=request.user, status="DISPUTED")
    demand_notices_resolved = Permit.objects.filter(company=request.user, status="RESOLVED")
    context = {
         "is_profile_complete" : False,
         "demand_notices": demand_notices,
         "demand_notices_paid": demand_notices_paid,
         "demand_notices_unpaid": demand_notices_unpaid,
        "demand_notices_disputed": demand_notices_disputed,
        "demand_notices_resolved": demand_notices_resolved,
    }
    return render(request, 'tax-payers/demand_notices.html', context)

@login_required
def disputes(request):
    user = User.objects.get(id = request.user.id)
    context = {
        "user":user
    }
    return render(request, 'tax-payers/disputes.html', context)


def infrastructures(request):
    demand_notices = Permit.objects.filter(company=request.user, infra_type = "Mast")
    demand_notices_paid = Permit.objects.filter(company=request.user, infra_type = "", status="PAID")
    demand_notices_unpaid = Permit.objects.filter(company=request.user, infra_type = "", status="UNPAID")
    demand_notices_disputed = Permit.objects.filter(company=request.user, infra_type = "", status="DISPUTED")
    demand_notices_resolved = Permit.objects.filter(company=request.user, infra_type = "", status="RESOLVED")
    context = {
         "is_profile_complete" : False,
         "demand_notices": demand_notices,
         "demand_notices_paid": demand_notices_paid,
         "demand_notices_unpaid": demand_notices_unpaid,
        "demand_notices_disputed": demand_notices_disputed,
        "demand_notices_resolved": demand_notices_resolved,
    }
    return render(request, 'tax-payers/infrastructure.html', context)


def downloads(request):
    context = {}
    return render(request, 'tax-payers/downloads.html', context)


def settings(request):
    context = {}
    return render(request, 'tax-payers/settings.html', context)


def resources(request):
    context = {}
    return render(request, 'tax-payers/resources.html', context)


def upload_existing_facilities(request):
    context = {}
    return render(request, 'tax-payers/upload-existing-facility.html', context)


def demand_notice_receipt(request, ref_id):
    permits = Permit.objects.filter(referenceid = ref_id, is_disputed=False)
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

    tot_sum_infra = Permit.objects.filter(referenceid = ref_id).aggregate(no_sum = Sum('infra_cost'))

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


def dispute_demand_notice_receipt(request, ref_id):
    print("DN - REF ID: ", ref_id)
    permits = Permit.objects.filter(referenceid = ref_id, is_disputed=True)
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

    tot_sum_infra = Permit.objects.filter(referenceid = ref_id, is_disputed=True).aggregate(no_sum = Sum('infra_cost'))

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
    return render(request, 'tax-payers/undisputed-receipt.html', context)

