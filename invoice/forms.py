from django import forms
from .models import *

class InvoiceForm(forms.Form):
	client = forms.CharField()
	mobile_number = forms.CharField(required=False)
	email_address = forms.CharField(required=False)
	address = forms.CharField(required=False)


class SaleItemForm(forms.Form):
	item = forms.CharField()
	description = forms.CharField(required=False)
	quantity = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control quantity', 'style': 'text-align: right'}),
                  	error_messages={'required': 'This field is required.'}, localize=True)
	unit_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control price', 'style': 'text-align: right'}),
                  	error_messages={'required': 'This field is required.'}, localize=True, required=False)
	vat_rate = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control vat', 'style': 'text-align: right'}),
                  	error_messages={'required': 'This field is required.'}, localize=True, required=False)


class InvoicePaymentForm(forms.Form):
	paid_amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control vat', 'style': 'text-align: right'}),
                  	error_messages={'required': 'This field is required.'}, localize=True, required=False)