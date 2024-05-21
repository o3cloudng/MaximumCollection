from django.db import models
from account.models import User
import uuid
    

class Permit(models.Model):
    company = models.ForeignKey(User, related_name="company", on_delete=models.CASCADE, null=False)
    referenceid = models.CharField(max_length=200, null=False)
    infra_type = models.CharField(max_length=200, null=False)
    add_from = models.CharField(max_length=200, null=False)
    add_to = models.CharField(max_length=200, null=False)
    length = models.CharField(max_length=200, null=True)
    year_installed = models.DateField(max_length=200, null=False)
    upload_application_letter = models.FileField(upload_to='uploads/applications/', null=False)
    upload_asBuilt_drawing = models.FileField(upload_to='uploads/drawings/', null=False)
    upload_payment_receipt = models.FileField(upload_to='uploads/receipts/', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.infra_type
    

class InfrastructureType(models.Model):
    infra_name = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.infra_name