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
from tax.resources import PermitResource
from tablib import Dataset
import csv, io
from tax.views.view_existing_infrastructure import generate_ref_id

def upload_new(request):
    if Permit.objects.all().exists(): 
        last = Permit.objects.latest("pk").id
        ref_id = "LA"+generate_ref_id() + str(last + 1).zfill(5)
    else:
        ref_id = "LA"+generate_ref_id() + "00001"

    if request.method == 'POST':
        permit_resource = PermitResource()
        dataset = Dataset()
        existing_permit = request.FILES['upload_csv_xlxs']

        if not Q(existing_permit.name.endswith('csv')) | Q(existing_permit.name.endswith('xlxs')):
            messages.error(request, 'Please, upload a csv or xlxs file only')
            return render(request, 'tax-payers/existing_infra_temp/apply_for_exist.html')
        else:
            messages.success(request, 'File successfully uploaded.')

        data_set = existing_permit.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimeter=',', quotechar="|"):
            created = Permit.objects.update_or_create(
                refrenceid = request.POST['referenceid'],
                company = request.user,
                is_existing = False,
                is_disputed = False,
                is_revised = False,
                infra_type=column[0],
                amount=column[1],
                length=column[2],
                add_from=column[3],
                add_to=column[4],
                year_installed=column[5],
                upload_application_letter=column[6],
                upload_asBuilt_drawing=column[7],
                # upload_payment_receipt=column[8],
            )
    return render(request, )