from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import User, AdminSetting
from tax.models import Permit, InfrastructureType, Waver
from datetime import date, timedelta
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django_htmx.http import HttpResponseClientRedirect
from django.db.models import Q, Count, Avg, Sum, Max


@login_required
def dashboard(request):
    user = User.objects.get(id = request.user.id)
    if user.is_profile_complete:
        context = {
            "is_profile_complete" : True,
            "user":user
        }

    demand_notices = Permit.objects.values('referenceid', 'is_disputed', 'is_revised').filter(Q(company=request.user)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_paid = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_paid=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_unpaid = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_paid=False)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_disputed = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_disputed=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_resolved = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_revised=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    # print("DN: ", demand_notices)
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
    demand_notices = Permit.objects.values('referenceid', 'is_disputed', 'is_revised').filter(Q(company=request.user)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_paid = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_paid=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_unpaid = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_paid=False)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_disputed = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_disputed=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    demand_notices_resolved = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_revised=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    # print("DN: ", demand_notices)
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
def infrastructures(request):
    # infrastructures = Permit.objects.values('infra_type', 'referenceid').filter(Q(company=request.user.id) & Q(infra_type__infra_name__icontains="mast")).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    coy = Q(company=request.user.id)
    roof_masts = (Q(infra_type__infra_name__icontains="mast") | Q(infra_type__infra_name__icontains="roof"))
    is_disp = Q(is_disputed = True)
    masts = Permit.objects.filter(coy & is_disp & roof_masts)
    fibre = Permit.objects.filter(coy & is_disp & Q(infra_type__infra_name__icontains="fibre"))
    power_line = Permit.objects.filter(coy & is_disp & Q(infra_type__infra_name__icontains="power"))
    pipeline = Permit.objects.filter(coy & is_disp & Q(infra_type__infra_name__icontains="pipe"))
    gas = Permit.objects.filter(coy & is_disp & Q(infra_type__infra_name__icontains="gas"))

    mast_roof_count = masts.aggregate(no_m = Sum('amount'))
    # fibre_count = fibre.count()
    # power_count = power_line.count()
    # pipe_count = pipeline.count()
    # gas_count = gas.count()
    # print("SUM OF MASTS: ", mast_count, "----- Fibre: ", fibre_count, "-----Power: ", power_count, "---Pipeline: ", pipe_count, "---Gas: ", gas_count)
    print("SUM OF MASTS: ", mast_roof_count['no_m'])
    context = {
        "infrastructures": infrastructures,
         "masts": masts,
         "mast_roof_count": mast_roof_count['no_m'],
         "fibre": fibre,
        "power_line": power_line,
        "pipeline": pipeline,
        "gas": gas
    }
    return render(request, 'tax-payers/infrastructure.html', context)


@login_required
def disputes(request):
    dispute_notices = Permit.objects.values('referenceid', 'is_disputed', 'is_revised').filter(Q(company=request.user) & Q(is_disputed=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    dispute_notices_paid = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_paid=True) & Q(is_disputed=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    dispute_notices_unpaid = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_paid=False) & Q(is_disputed=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    dispute_notices_disputed = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_disputed=True) & Q(is_disputed=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    dispute_notices_resolved = Permit.objects.values('referenceid').filter(Q(company=request.user) & Q(is_revised=True) & Q(is_disputed=True)).annotate(total=Count('id'), created_at=Max('created_at')).order_by('-created_at')
    # print("DN: ", demand_notices)
    context = {
         "is_profile_complete" : False,
         "dispute_notices": dispute_notices,
         "dispute_notices_paid": dispute_notices_paid,
         "dispute_notices_unpaid": dispute_notices_unpaid,
        "dispute_notices_disputed": dispute_notices_disputed,
        "dispute_notices_resolved": dispute_notices_resolved,
    }
    return render(request, 'tax-payers/disputes.html', context)

@login_required
def downloads(request):
    files = Permit.objects.filter(company=request.user)
    print("FILE: ", files)
    for file in files:
        print("File Here", file.referenceid)
        print("File Here", file.upload_application_letter)
        print("File Here", file.infra_type)

    context = {
        "files": files
    }
    return render(request, 'tax-payers/downloads.html', context)


