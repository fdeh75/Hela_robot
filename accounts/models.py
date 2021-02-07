from django.contrib import admin
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, UserManager
)

from plats_bank.models import Job_type


class MyUserManager(BaseUserManager):
    # def create_user(self, email, date_of_birth, password=None):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # city=self.city
            # date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, date_of_birth, password=None):
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Experiences(models.Model):
    user = models.ForeignKey('accounts.MyUser', blank=True, null=True, on_delete=models.SET_NULL)
    company = models.CharField(max_length=20, blank=True, default='', null=True)
    title = models.CharField(max_length=100, default='', blank=True, null=True)
    place = models.CharField(max_length=100, default='', blank=True, null=True)
    between = models.CharField(max_length=100, default='', blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)

    class Meta:
        verbose_name = 'Erfarenheter'
        verbose_name_plural = 'Erfarenheter'

    def __str__(self):
        return str(self.title) + " <=> " + str(self.user.f_name) + " " + str(self.user.l_name)


class Employments(models.Model):
    user = models.ForeignKey('accounts.MyUser', blank=True, null=True, on_delete=models.SET_NULL)
    company = models.CharField(max_length=20, blank=True, default='', null=True)
    title = models.CharField(max_length=100, default='', blank=True, null=True)
    place = models.CharField(max_length=100, default='', blank=True, null=True)
    between = models.CharField(max_length=100, default='', blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)

    class Meta:
        verbose_name = 'Anställningar'
        verbose_name_plural = 'Anställningar'

    def __str__(self):
        return str(self.title) + " <=> " + str(self.user.f_name) + " " + str(self.user.l_name)


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True)
    phone = models.CharField(max_length=20, blank=True, default='', null=True)
    f_name = models.CharField(max_length=100, default='', blank=True, null=True)
    l_name = models.CharField(max_length=100, default='', blank=True, null=True)
    organization = models.CharField(max_length=100, default='', blank=True, null=True)
    street = models.CharField(max_length=20, blank=True, default='', null=True)
    zip_code = models.CharField(max_length=100, default='', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    city = models.ForeignKey('plats_bank.City', on_delete=models.SET_NULL,
                             null=True, blank=True)
    jobb_type = models.ManyToManyField('plats_bank.Job_type',
                                       null=False, blank=True)

    career_profile = models.TextField(null=False, blank=True)
    # EXPERIENCES
    experience = models.ManyToManyField('accounts.Experiences',
                                        null=False, blank=True)
    # Employments
    employment_des = models.TextField(null=False, blank=True)
    employment = models.ManyToManyField('accounts.Employments',
                                         null=False, blank=True)

    send_email = models.BooleanField(default=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
