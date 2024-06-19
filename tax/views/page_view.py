from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import User, AdminSetting
from tax.models import Permit, InfrastructureType, Waver
from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django_htmx.http import HttpResponseClientRedirect
from django.db.models import Q, Count, Avg, Sum, Max
from django.http import HttpResponse


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
    demand_notices = Permit.objects.filter(company=request.user.id)
    demand_notices_paid = Permit.objects.filter(company=request.user.id, status="PAID")
    demand_notices_unpaid = Permit.objects.filter(company=request.user.id, status="UNPAID")
    demand_notices_disputed = Permit.objects.filter(company=request.user.id, status="DISPUTED")
    demand_notices_resolved = Permit.objects.filter(company=request.user.id, status="RESOLVED")
    context = {
         "is_profile_complete" : False,
         "demand_notices": demand_notices,
         "demand_notices_paid": demand_notices_paid,
         "demand_notices_unpaid": demand_notices_unpaid,
        "demand_notices_disputed": demand_notices_disputed,
        "demand_notices_resolved": demand_notices_resolved,
    }
    return render(request, 'tax-payers/infrastructure.html', context)


@login_required
def disputes(request):
    user = User.objects.get(id = request.user.id)
    context = {
        "user":user
    }
    return render(request, 'tax-payers/disputes.html', context)

@login_required
def downloads(request):
    context = {}
    return render(request, 'tax-payers/downloads.html', context)

@login_required
def settings(request):
    context = {}
    return render(request, 'tax-payers/settings.html', context)
