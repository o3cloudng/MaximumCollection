from django.shortcuts import render, redirect
from tax.forms import PermitForm, PermitEditForm, WaverForm, RemittanceForm
from django.contrib.auth.decorators import login_required
from account.models import User, AdminSetting
from tax.models import Permit, InfrastructureType, Waver, Remittance
from datetime import date, timedelta, datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django_htmx.http import HttpResponseClientRedirect
from django.db.models import F, Q, Count, Avg, Sum
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.http import HttpResponse
from django.contrib import messages


@login_required
def apply_for_waver(request):
    if request.method == 'POST':
        if Waver.objects.filter(Q(company=request.user) & Q(referenceid=request.POST.get('referenceid'))).exists():
            messages.error(request, 'You have already applied for waver.')
            return redirect('dispute-ex-demand-notice', request.POST.get('referenceid'))

        form = WaverForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            print("WAVER HERE FORM IS VALID ")
            wave = form.save(commit=False)
            wave.referenceid = request.POST.get('referenceid')
            wave.company = request.user
            wave.save()

            messages.success(request, 'Your request for waver was sent successfully.')
            return redirect('dispute-ex-demand-notice', request.POST.get('referenceid'))
        else:
            print("FILE FORMAT INVALID", form.errors)
      
        messages.error(request, 'Your request for waver failed.')
        return redirect('dispute-ex-demand-notice', request.POST.get('referenceid'))

@login_required
def apply_remittance(request):
    if request.method == 'POST':
        if Remittance.objects.filter(Q(company=request.user) & Q(referenceid=request.POST.get('referenceid'))).exists():
            messages.error(request, 'You have already applied for waver.')
            return redirect('dispute-ex-demand-notice', request.POST.get('referenceid'))

        form = RemittanceForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            print("WAVER HERE FORM IS VALID ")
            remittance = form.save(commit=False)
            remittance.referenceid = request.POST.get('referenceid')
            remittance.company = request.user
            remittance.apply_for_waver = request.POST.get('apply_for_waver')
            remittance.save()

            messages.success(request, 'Your remiitance was added successfully.')
            return redirect('dispute-ex-demand-notice', request.POST.get('referenceid'))
        else:
            print("FILE FORMAT INVALID", form.errors)
      
        messages.error(request, 'Your remittance failed.')
        return redirect('dispute-ex-demand-notice', request.POST.get('referenceid'))


def generate_ref_id():
    today = date.today()
    year = str(today.year)
    month = str(today.month).zfill(2)
    return year+month


# Calculate penalty function
# penalty_fee, number of days per infrastructure
# day * years
def age(the_date):
    date_format = "%m/%d/%Y"

    a = datetime.strptime(the_date, date_format)
    b = datetime.now()

    delta = b - a
    return delta.days


@login_required
def apply_for_existing_permit(request):
    if Permit.objects.all().exists(): 
        last = Permit.objects.latest("pk").id
        ref_id = "LA"+generate_ref_id() + str(last + 1).zfill(5)
    else:
        ref_id = "LA"+generate_ref_id() + "00001"

    print("EXISITING: APPLY FOR EXISTING PERMIT")

    if request.htmx:
        print("REF: ", ref_id)
        form = PermitForm(request.POST or None, request.FILES or None)

        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])
        print("READY POST: ", infra_rate.rate, type(infra_rate.rate))
        print("Permit type: ", request.POST['amount'], type(request.POST['amount']))

        if "mast" in infra_rate.infra_name.lower():
            len = 0
            qty = request.POST['amount']
            infra_cost = infra_rate.rate * int(request.POST['amount'])
        elif "roof" in infra_rate.infra_name.lower():
            len = 0
            qty = request.POST['amount']
            infra_cost = infra_rate.rate * int(request.POST['amount'])
        else:
            infra_cost = infra_rate.rate * int(request.POST['length'])
            len = request.POST['length']
            qty = 0

        # print("AMOUNT OR NUMBER: ", infra_rate.infra_name.lower())

        if form.is_valid():
            # print("Form is valid")
            permit = form.save(commit=False)
            permit.referenceid = request.POST['reference']
            permit.company = request.user
            permit.amount = qty
            permit.length = len
            # permit.age = age
            permit.is_existing = True
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

    if request.htmx:
        return HttpResponseClientRedirect('/tax/apply/permit/demand_notice_ex/receipt/'+permit.referenceid)

    return render(request, 'tax-payers/existing_infra_temp/apply_for_exist.html', context)


@login_required
def add_permit_ex_form(request):
    print("ADDING EXISITING INFRASTRUCTURE")
    if Permit.objects.all().exists(): 
        last = Permit.objects.latest("pk").id
        ref_id = "LA"+generate_ref_id() + str(last + 1).zfill(5)
    else:
        ref_id = "LA"+generate_ref_id() + "00001"
    
    permits = Permit.objects.all()
    if request.method == "POST":
        form = PermitForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.referenceid = ref_id
            permit.company = request.user
            permit.is_existing = True
            permit.save()
            permits = Permit.objects.all()
            context = {
                'permits': permits
            }

            return render(request, 'tax-payers/partials/permit_details.html', context)
        else:
            print("ERROR: ", form.errors)

    context = {
        'form':form,
        'referenceid': ref_id,
        'company': request.user
    }
    return render(request, 'tax-payers/partials/apply_permit_ex_form.html', context)


# Receipt (DN)
@login_required
def demand_notice_ex_receipt(request, ref_id):
    permits = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_disputed=False) & Q(is_existing=True))

    if not permits.exists(): # If permit does not exist
        return redirect('apply_for_permit')
    
    if not permits.first().company == request.user: # If permite does not belong to signed in company
        return redirect('apply_for_permit')
    
    ref = permits.first()
    app_fee = AdminSetting.objects.get(slug="application-fee")
    site_assessment = AdminSetting.objects.get(slug="site-assessment")
    admin_pm_fees = AdminSetting.objects.get(slug="admin-pm-fees")
    penalty = AdminSetting.objects.get(slug="penalty")

    mast_roof = Permit.objects.filter((Q(referenceid = ref_id) & Q(is_disputed=False) & Q(is_existing=True)) & (Q(infra_type__infra_name__istartswith='Mast') | Q(infra_type__infra_name__istartswith='Roof')))
    
    length = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_disputed=False) & Q(is_existing=True) & (Q(infra_type__infra_name__istartswith='Optic') | Q(infra_type__infra_name__istartswith='Gas') | Q(infra_type__infra_name__istartswith='Power') | Q(infra_type__infra_name__istartswith='Pipeline')))
    #application number = number of masts and rooftops 

    if mast_roof.exists():
        mast_roof_no = mast_roof.aggregate(no_sites = Sum('amount'))['no_sites']
    else:
        mast_roof_no = 0
        # mast_roof_no['no_sites'] = 0

    # print("MAST & ROOF NO: ", mast_roof.count())
    if length.exists():
        app_count = mast_roof_no + length.count()
    else:
        app_count = mast_roof_no + 0

    total_app_fee = app_count * app_fee.rate

    tot_sum_infra = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_existing=True)).aggregate(no_sum = Sum('infra_cost'))

    # Site assessment report rate
    sar_rate = mast_roof_no * site_assessment.rate
    # print("SUM: ", tot_sum_infra['no_sum'], type(tot_sum_infra['no_sum']))


    admin_pm_fees_sum = (admin_pm_fees.rate * tot_sum_infra['no_sum']) / 100

    total_due = tot_sum_infra['no_sum'] + total_app_fee + admin_pm_fees_sum + sar_rate

    # print("ADMIN FEE: ", total_due, type(total_due))
    # ADD WAVER
    if Waver.objects.filter(referenceid=ref).exists():
        waver = Waver.objects.get(referenceid=ref).wave_amount
    else:
        waver = 0
    # PENALTY CALCULATION
    refid = Q(referenceid = ref_id)
    is_exist = Q(is_existing=True)
    not_dispute = Q(is_disputed=False)
    # current_user = Q(comapny = request.user)
    if Permit.objects.filter(refid & is_exist).exists():
        age_sum = Permit.objects.filter(refid & is_exist & not_dispute).aggregate(ages = Sum('age'))['ages']
    else:
        age_sum = 0

    # print("AGE Calculated: ", age_sum)
    
    penalty_sum = age_sum * penalty.rate
    # print("PENALTY Calculated: ", penalty_sum)

    
    # print("WAVER: ", waver)
    total_liability = total_due + penalty_sum - waver

    # Testing Model @property
    # new_cum_age = Permit.objects.filter(refid & is_exist & not_dispute)
    # new_cum_age = new_cum_age.annotate(age_now = F('updated_cum_age')).aggregate(total=Sum('age_now'))
    # print("NEW CUM AGE: ", new_cum_age)
    

    context = {
        'permits': permits,
        'ref': ref,
        'site_assessment': site_assessment,
        'site_assess_count': mast_roof_no,
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
        'penalty_sum': penalty_sum,
        'penalty': penalty,
        'age_sum': age_sum
    }
    return render(request, 'tax-payers/receipts/demand-notice-ex-receipt .html', context)


@login_required # Dispute Demand Notice - Issues
def dispute_ex_demand_notice(request, ref_id):

    form = RemittanceForm()

    ref = Q(referenceid=ref_id)
    coy = Q(company=request.user)
    is_dis = Q(is_disputed = False)
    not_dis = Q(is_disputed = True)
    is_existing = Q(is_existing = True)
    permits = Permit.objects.filter(ref & coy & is_dis & is_existing)
    undisputed_permits = Permit.objects.filter(ref & coy & not_dis & is_existing)
    # print("PERMIT COUNT: ", permits)
    # print("UNDISPUTED COUNT: ", undisputed_permits)
    
    # if request.method == "POST":
        # print("POST SHOWS HERE....")
    remittance = Remittance.objects.get(Q(referenceid=ref_id) & Q(company=request.user))
   
    context = {
        'ref_id': ref_id,
        'permits': permits,
        'undisputed_permits': undisputed_permits,
        'remittance': remittance,
        'form': form
    }
    return render(request, 'tax-payers/existing_infra_temp/apply_for_ex_permit_edit.html', context)


@login_required
def undispute_ex_demand_notice_receipt(request, ref_id):
    permits = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_disputed=True) & Q(is_existing=True))

    if not permits.exists():
        return redirect('apply_existing_infra')

    if not permits.first().company == request.user:
        return redirect('apply_existing_infra')
    
    ref = permits.first()
    app_fee = AdminSetting.objects.get(slug="application-fee")
    site_assessment = AdminSetting.objects.get(slug="site-assessment")
    admin_pm_fees = AdminSetting.objects.get(slug="admin-pm-fees")
    penalty = AdminSetting.objects.get(slug="penalty")

    mast_roof = Permit.objects.filter((Q(referenceid = ref_id) & Q(is_disputed=True) & Q(is_existing=True)) & (Q(infra_type__infra_name__istartswith='Mast') | Q(infra_type__infra_name__istartswith='Roof')))
    
    length = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_disputed=True) & Q(is_existing=True) & (Q(infra_type__infra_name__istartswith='Optic') | Q(infra_type__infra_name__istartswith='Gas') | Q(infra_type__infra_name__istartswith='Power') | Q(infra_type__infra_name__istartswith='Pipeline')))
    #application number = number of masts and rooftops 

    remittance = Remittance.objects.get(Q(referenceid=ref_id) & Q(company=request.user))

    if mast_roof.exists():
        mast_roof_no = mast_roof.aggregate(no_sites = Sum('amount'))['no_sites']
    else:
        mast_roof_no = 0
        # mast_roof_no['no_sites'] = 0

    print("MAST & ROOF NO: ", mast_roof_no)
    if length.exists():
        len_count = length.count()
    else:
        len_count = 0

    app_count = mast_roof_no + len_count
    total_app_fee = app_count * app_fee.rate

    tot_sum_infra = Permit.objects.filter(Q(referenceid = ref_id) & Q(is_existing=True)).aggregate(no_sum = Sum('infra_cost'))

    # Site assessment report rate
    sar_rate = mast_roof_no * site_assessment.rate
    # print("SUM: ", tot_sum_infra['no_sum'], type(tot_sum_infra['no_sum']))


    admin_pm_fees_sum = (admin_pm_fees.rate * tot_sum_infra['no_sum']) / 100

    total_due = tot_sum_infra['no_sum'] + total_app_fee + admin_pm_fees_sum + sar_rate

    print("ADMIN FEE: ", total_due, type(total_due))
    # ADD WAVER
    if Waver.objects.filter(referenceid=ref).exists():
        waver = Waver.objects.get(referenceid=ref).wave_amount
    else:
        waver = 0
    # PENALTY CALCULATION
    refid = Q(referenceid = ref_id)
    is_exist = Q(is_existing=True)
    is_dispute = Q(is_disputed=True)
    # current_user = Q(comapny = request.user)
    if Permit.objects.filter(refid & is_exist).exists():
        age_sum = Permit.objects.filter(refid & is_exist & is_dispute).aggregate(ages = Sum('age'))['ages']
    else:
        age_sum = 0

    print("AGE Calculated: ", age_sum)
    
    penalty_sum = age_sum * penalty.rate
    print("PENALTY Calculated: ", penalty_sum)

    print("REMITTANCE: ", remittance)

    # print("NEW CUMMULATIVE AGES: ", cum_ages['cummulative_age'])

    
    # print("WAVER: ", waver)
    total_liability = total_due + penalty_sum - remittance.remitted_amount - waver
    

    context = {
        'permits': permits,
        'ref': ref,
        'site_assessment': site_assessment,
        'site_assess_count': mast_roof_no,
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
        'penalty_sum': penalty_sum,
        'penalty': penalty,
        'remittance': remittance,
        'age_sum': age_sum
    }
    return render(request, 'tax-payers/receipts/undisputed_ex_dn_receipt.html', context)


@login_required
def add_dispute_ex_dn_edit(request):
    ref_id = str(request.POST['referenceid'])
    # print("REF: ", ref_id)
    if request.method == 'POST':
        form = PermitEditForm(request.POST or None, request.FILES or None)

        infra_rate = InfrastructureType.objects.get(pk=request.POST['infra_type'])
        # print("READY POST: ", infra_rate.rate, type(infra_rate.rate))
        # print("Permit type: ", request.POST['amount'], type(request.POST['amount']))
        if "mast" in infra_rate.infra_name.lower():
            # infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        elif "roof" in infra_rate.infra_name.lower():
            # infra_cost = infra_rate.rate * int(request.POST['amount'])
            len = 0
            qty = request.POST['amount']
        else:
            # infra_cost = infra_rate.rate * int(request.POST['length'])
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
            # permit.infra_cost = infra_cost
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
