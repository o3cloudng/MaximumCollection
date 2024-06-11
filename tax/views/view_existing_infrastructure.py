from django.shortcuts import render, redirect
from tax.forms import PermitForm, PermitEditForm
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


def generate_ref_id():
    today = date.today()
    year = str(today.year)
    month = str(today.month).zfill(2)
    return year+month

@login_required
def apply_for_existing_permit(request):
    if Permit.objects.all().exists(): 
        last = Permit.objects.latest("pk").id
        ref_id = "LA"+generate_ref_id() + str(last + 1).zfill(5)
    else:
        ref_id = generate_ref_id() + "00001"

    print("WE ARE HERE...")

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
            permit.is_existing = True
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
        return HttpResponseClientRedirect('/tax/apply/permit/demand_notice_ex/receipt/'+permit.referenceid)

    return render(request, 'tax-payers/existing_infra_temp/apply_for_exist.html', context)


@login_required
def add_permit_ex_form(request):
    
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
    return render(request, 'tax-payers/partials/apply_permit_ex_form.html', context)


def demand_notice_ex_receipt(request, ref_id):
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
    return render(request, 'tax-payers/receipts/demand-notice-ex-receipt .html', context)


@login_required
def dispute_ex_demand_notice(request, ref_id):

    ref = Q(referenceid=ref_id)
    coy = Q(company=request.user)
    is_dis = Q(is_disputed = False)
    not_dis = Q(is_disputed = True)
    is_existing = Q(is_existing = True)
    permits = Permit.objects.filter(ref & coy & is_dis & is_existing)
    undisputed_permits = Permit.objects.filter(ref & coy & not_dis & is_existing)
    print("PERMIT COUNT: ", permits)
    print("UNDISPUTED COUNT: ", undisputed_permits)
    
    if request.method == "POST":
        print("POST SHOWS HERE....")
   
    context = {
        'ref_id': ref_id,
        'permits': permits,
        'undisputed_permits': undisputed_permits
    }
    return render(request, 'tax-payers/existing_infra_temp/apply_for_ex_permit_edit.html', context)


@login_required
def undispute_ex_demand_notice_receipt(request, ref_id):
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
    return render(request, 'tax-payers/receipts/undisputed_ex_dn_receipt.html', context)


@login_required
def add_dispute_ex_dn_edit(request):
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
def dispute_ex_dn_edit(request, pk):
    permit = Permit.objects.get(pk=pk)
    form = PermitEditForm(instance = permit)
    context = {
        'form': form
    }
    return render(request, 'tax-payers/partials/apply_ex_permit_edit_form.html', context)
