from django.shortcuts import render, redirect
from tax.forms import PermitForm
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Permit


@login_required
def apply_for_permit(request):
    if request.method == "POST":
        form = PermitForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            return redirect("demand-notice")
        
        else:
            print("FILE FORMAT INVALID")
    form = PermitForm()

    context = {
        'form':form
    }

    return render(request, 'tax-payers/apply_for_permit.html', context)

@login_required
def demand_notice(request):
    user = User.objects.get(id=request.user.id)
    context = {
        "user": user
    }
    return render(request, 'tax-payers/demand_notice.html', context)

@login_required
def add_permit_form(request):
    # user = User.objects.get(id=request.user.id)
    permits = Permit.objects.all()
    if request.method == "POST":
        form = PermitForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.company = request.user
            permit.save()
            permits = Permit.objects.all()
            context = {
                'permits': permits
            }

            print("USER ID: ", permits)
            return render(request, 'tax-payers/partials/permit_details.html', context)

    context = {
        "form": PermitForm(request.POST),
        "permits" : permits
    }
    return render(request, 'tax-payers/partials/apply_permit_form.html', context)


@login_required
def dashboard(request):
    user = User.objects.get(id = request.user.id)
    context = {
        "user":user
    }
    return render(request, 'tax-payers/dashboard.html', context)


@login_required
def disputes(request):
    user = User.objects.get(id = request.user.id)
    context = {
        "user":user
    }
    return render(request, 'tax-payers/disputes.html', context)


def template(request):
    context = {}
    return render(request, 'tax-payers/template.html', context)