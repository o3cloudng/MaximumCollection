from django.db import models
from account.models import User
import uuid
    

class Permit(models.Model):
    PAY_CHOICES = (
        ("UNPAID", "Unpaid"),
        ("PAID", "Paid"),
        ("DISPUTED", "Disputed"),
        ("RESOLVED", "Resolved"),
    )
    company = models.ForeignKey(User, related_name="company", on_delete=models.CASCADE, null=True)
    referenceid = models.CharField(max_length=200, null=True) 
    infra_type = models.CharField(max_length=200, null=False)
    amount = models.CharField(max_length=200, null=False) 
    length = models.CharField(max_length=200, null=True)
    add_from = models.CharField(max_length=200, null=False)
    add_to = models.CharField(max_length=200, null=False)
    year_installed = models.DateField(max_length=200, null=False)
    upload_application_letter = models.FileField(upload_to='uploads/applications/', blank=True, null=True)
    upload_asBuilt_drawing = models.FileField(upload_to='uploads/drawings/', blank=True, null=True)
    upload_payment_receipt = models.FileField(upload_to='uploads/receipts/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=PAY_CHOICES, default="UNPAID")
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company} - {self.referenceid}"
    

class InfrastructureType(models.Model):
    infra_name = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.infra_name