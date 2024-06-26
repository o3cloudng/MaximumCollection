from django.db import models

from django.db import models
from helpers.models import TrackingModel

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from enum import Enum
import uuid
from django.utils.text import slugify


class Sector(models.Model):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# CREATE CUSTOM USER MANAGER TO BE EXTENDED BY USER
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", False)
        if email is None:
            raise TypeError(_("User should have an Email"))

        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser True")

        return self.create_user(email=email, password=password, **extra_fields)


# MY CUSTOM USER
class User(AbstractUser, TrackingModel, PermissionsMixin):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=255, unique=True)
    company_name = models.CharField(max_length=200)
    username = models.CharField(max_length=255, null=True, )
    rc_number = models.CharField(max_length=20)
    phone_number = PhoneNumberField(blank=True)
    country = models.CharField(max_length=300, default="Nigeria")
    state = models.CharField(max_length=300, default="Lagos State")
    address = models.CharField(max_length=300)
    company_logo = models.ImageField(upload_to='uploads/logo/', blank=True, default='uploads/default.png')
    postal_code = models.CharField(max_length=300)
    bio_data = models.TextField(blank=True)
    date_enrolled = models.DateField(blank=True, null=True)
    sector = models.ForeignKey(Sector, related_name="sector", on_delete=models.CASCADE, null=True)
    is_tax_admin = models.BooleanField(default=False)
    is_profile_complete = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    # def get_absolute_url(self, *args, **kwargs):
    #     return reverse("User:detail", kwargs={"email": self.email})

class AdminSetting(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(null=True, default="slug")
    description = models.CharField(max_length=200)
    rate = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(AdminSetting, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.rate}"
