from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from google.oauth2.credentials import Credentials
from django.contrib import admin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=70,unique=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name','email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Questions(models.Model):
    CHOICES = [
        ('SPORTS','SPORTS'),
        ('GEOGRAPHY','GEOGRAPHY'),
        ('HISTORY','HISTORY'),
        ('MOVIES','MOVIES'),
        ('MUSIC','MUSIC'),
        ('LITERATURE','LITERATURE'),
    ]

    OPTIONS = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
    ]

    question=models.CharField(max_length=254)
    opt_a=models.CharField(max_length=254)
    opt_b=models.CharField(max_length=254)
    opt_c=models.CharField(max_length=254)
    opt_d=models.CharField(max_length=254)
    category=models.CharField(choices=CHOICES,default=None,max_length=15)
    answer=models.CharField(choices=OPTIONS,default=None,max_length=15)
    published=models.BooleanField(default=False,null=True)

class Scores(models.Model):
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6,decimal_places=3)
    category = models.CharField(max_length=15)

class Leaderboard(models.Model):
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6,decimal_places=3)
    

