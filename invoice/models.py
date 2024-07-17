from django.db import models
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from datetime import date
from decimal import *
import decimal, datetime
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from datetime import timedelta
from django.db.models import Sum
import os
from django.conf import settings
today = date.today()

class Organization(models.Model):
    name =  models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=20)
    email_address = models.CharField(max_length=100)
    address = models.TextField()
    logo = models.FileField(upload_to="logo/%Y/%m/%d",null=True,blank=True)

    def __str__(self):
        return self.name

    def get_logo_path(self):
        if self.logo:
            return os.path.join(settings.MEDIA_ROOT,self.logo.path)
        return get_logo_path

    def detail(self, **kwargs):
        detail = "<span style='font-size: 1.5em; color: darkblue; text-align: left !important; padding-bottom: 5px;'>" + self.name + '</span>' + \
            '\n' + self.mobile_number + " | " + self.email_address + '\n' + self.address
        return detail

class Invoice(models.Model):
    client =  models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=20)
    email_address = models.CharField(max_length=100)
    address = models.TextField()
    date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True,blank=True)
    amount = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    vat = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    status = models.CharField(max_length=20,default='pending')
    currency = models.CharField(max_length=20,default='USD')
    term = models.IntegerField(default=1)
    paid_amount = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    remaining_amount = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)

    def save(self, *args, **kwargs):
        d = timedelta(days=self.term)
        self.due_date = self.date + d
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return self.client


class SaleItem(models.Model):
    invoice = models.ForeignKey(Invoice,related_name='saleitem',on_delete=models.SET_NULL,null=True,blank=True)
    item = models.CharField(max_length=250)
    description = models.TextField(null=True,blank=True)
    quantity = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    unit_price = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    price = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    vat_rate = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    vat = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)
    date = models.DateField(default=timezone.now)
    currency = models.CharField(max_length=20,default='KES')

    def save(self, *args, **kwargs):
        self.price = decimal.Decimal(self.quantity) * decimal.Decimal(self.unit_price)
        self.vat = decimal.Decimal(self.price) * decimal.Decimal(self.vat_rate/100)
        self.total = decimal.Decimal(self.price) + decimal.Decimal(self.vat)
        super(SaleItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.item


@receiver(post_save, sender=SaleItem)
def invoice_sales_total(sender, instance, created, **kwargs):
    if created:
        amount = SaleItem.objects.filter(invoice=instance.invoice).aggregate(Sum('price'))['price__sum']
        vat = SaleItem.objects.filter(invoice=instance.invoice).aggregate(Sum('vat'))['vat__sum']

        total = decimal.Decimal(amount) + decimal.Decimal(vat)
        Invoice.objects.filter(id=instance.invoice.id).update(amount=amount,vat=vat,total = total)