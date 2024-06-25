from django.db import models
from account.models import User
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from django.db.models import F, Q, Count, Avg, Sum
from queryable_properties.properties import queryable_property
    


class InfrastructureType(models.Model):
    infra_name = models.CharField(max_length=200, null=False)
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.infra_name
    

class Permit(models.Model):
    PAY_CHOICES = (
        ("UNPAID", "Unpaid"),
        ("PAID", "Paid"),
        ("DISPUTED", "Disputed"),
        ("Revised", "Revised"),
    )
    company = models.ForeignKey(User, related_name="company", on_delete=models.CASCADE, null=True)
    referenceid = models.CharField(max_length=200, null=True) 
    infra_type = models.ForeignKey(InfrastructureType, related_name="infra_type", on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, default=0) 
    length = models.IntegerField(null=True, default=0)
    add_from = models.CharField(max_length=200, blank=True)
    add_to = models.CharField(max_length=200, blank=True)
    year_installed = models.DateField(max_length=200, null=True)
    age = models.PositiveIntegerField(blank=True)
    upload_application_letter = models.FileField(upload_to='uploads/applications/', blank=True, null=True)
    upload_asBuilt_drawing = models.FileField(upload_to='uploads/drawings/', blank=True, null=True)
    upload_payment_receipt = models.FileField(upload_to='uploads/receipts/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=PAY_CHOICES, default="UNPAID")
    is_profile_complete = models.BooleanField(default=False)
    is_disputed = models.BooleanField(default=False)
    is_undisputed = models.BooleanField(default=False)
    is_revised = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_existing = models.BooleanField(default=False)
    infra_cost = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # generate Age from the year_installed field
        installed_date = datetime.strptime(str(self.year_installed), '%Y-%m-%d').date()
        today = date.today()
        age = (today - installed_date).days

        if "mast" in self.infra_type.infra_name.lower():
            cummulative_age = int(self.amount) * age
            # self.infra_cost = self.amount * self.infra_type.rate
        elif "roof" in self.infra_type.infra_name.lower():
            cummulative_age = int(self.amount) * age
            # self.infra_cost = self.amount * self.infra_type.rate
        else:
            cummulative_age = age

        self.age = cummulative_age
        print("AGE FROM DB: ", age, type(age), " | CUM AGE: ", cummulative_age, " | AMOUNT: ", type(self.amount), self.amount * age)
 
        super(Permit, self).save(*args, **kwargs)

    # @property
    @queryable_property
    def updated_cum_age(self):
        # updated_cum_age = ""
        installed_date = datetime.strptime(str(self.year_installed), '%Y-%m-%d').date()
        today = date.today()
        age = (today - installed_date).days
        if "mast" in self.infra_type.infra_name.lower():
            updated_cum_age = int(self.amount) * age
            # self.infra_cost = self.amount * self.infra_type.rate
        elif "roof" in self.infra_type.infra_name.lower():
            updated_cum_age = int(self.amount) * age
            # self.infra_cost = self.amount * self.infra_type.rate
        else:
            updated_cum_age = age

        print("CURRENT AGE IN DAYS: ", updated_cum_age)
        # Permit.objects.filter(refid & is_exist & not_dispute).annotate('updated_cum_age').aggregate(sum_age = Sum('updated_cum_age'))
        # cum_age = Permit.objects.annotate(sum_a_and_b=F('a') + F('b')).aggregate(total=Sum('sum_a_and_b'))
        # cum_age = Permit.objects.annotate(sum_a_and_b=F('a') + F('b')).aggregate(total=Sum('sum_a_and_b'))

        return updated_cum_age

    def __str__(self):
        if self.is_existing:
            prem = "Existing Infrastructure"
        else:
            prem = "New Infrastructure"
        return f"{self.referenceid} - ({prem}) ---- {self.infra_type} {self.age}"
    

class Waver(models.Model):
    referenceid = models.CharField(max_length=200, blank=False)
    company = models.ForeignKey(User, related_name="companyid", on_delete=models.CASCADE)
    wave_amount = models.IntegerField(default=0)
    receipt = models.FileField(upload_to='uploads/receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wave_amount}"
    

class Remittance(models.Model):
    referenceid = models.CharField(max_length=200, blank=False)
    company = models.ForeignKey(User, related_name="remit_comp", on_delete=models.CASCADE)
    remitted_amount = models.IntegerField(blank=True)
    receipt = models.FileField(upload_to='uploads/receipts/', blank=True, null=True)
    approved = models.BooleanField(default=False)
    apply_for_waver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.referenceid} - {self.remitted_amount}"
    