from django.db import models

class Waver(models.Model):
    referenceid = models.CharField(max_length=10, null=False)
    amount = models.PositiveIntegerField(max_length=200)
    is_approved = models.BooleanField(default=False)
    receipt = models.FileField(upload_to='uploads/receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return
