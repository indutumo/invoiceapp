from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.utils import timezone
import io, requests, datetime
from django.http import HttpResponse, JsonResponse
from .render import Render
today = date.today()
from django.db.models import Sum, Avg, F, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta


#creating invoice
def create_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            mobile_number = form.cleaned_data['mobile_number']
            email_address = form.cleaned_data['email_address']
            address = form.cleaned_data['address']

            invoice = Invoice(client=client,mobile_number=mobile_number,address=address,email_address=email_address)
            invoice.save()
            return redirect('add_item_invoice', pk=invoice.id)
        else:
            print(form.errors)
    else:
        form = InvoiceForm()
    context = {
    	'form': form
    	}
    return render(request, 'invoice/invoice_list.html', context)



def add_item_invoice(request,pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = SaleItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            description = form.cleaned_data['description']
            quantity = form.cleaned_data['quantity']
            unit_price = form.cleaned_data['unit_price']
            vat_rate = form.cleaned_data['vat_rate']

            SaleItem.objects.create(invoice=invoice,item=item,quantity=quantity,unit_price=unit_price,vat_rate=vat_rate,
                description=description)
            return redirect('add_item_invoice', pk=invoice.pk)
        else:
            print(form.errors)
    else:
        form = SaleItemForm()

    saleitem = SaleItem.objects.filter(invoice=invoice).order_by('id')
    context = {
            'form':form,
            'invoice': invoice,
            'saleitem': saleitem,
            }

    return render(request, 'invoice/invoice_item_form.html', context)


def invoice_payment(request,pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = InvoicePaymentForm(request.POST)
        if form.is_valid():
            paid_amount = form.cleaned_data['paid_amount']
            remaining_amount = decimal.Decimal(invoice.total) - decimal.Decimal(paid_amount)
            Invoice.objects.filter(id=invoice.id).update(paid_amount=paid_amount,remaining_amount=remaining_amount)
            return redirect('invoice_detail', pk=quote.pk)
        else:
            print(form.errors)
    else:
        form = InvoicePaymentForm()
    context = {
            'form':form,
            'invoice': invoice,            
            }
    return render(request, 'invoice/invoice_item_form.html', context)

def invoicepdf(request,pk):
    invoice = get_object_or_404(Invoice,pk=pk)
    saleitem = SaleItem.objects.filter(invoice=invoice).order_by('id')
    organization = Organization.objects.last()

    context = {
        'invoice':invoice,
        'saleitem':saleitem, 
        'organization':organization,
        }
    return Render.render('invoice/invoice_pdf.html', context)

def invoice_detail(request,pk):
    invoice = get_object_or_404(Invoice,pk=pk)
    saleitem = SaleItem.objects.filter(invoice=invoice).order_by('id')

    context = {
        'invoice':invoice,
        'saleitem':saleitem, 
        }
    return render(request,'invoice/invoice_detail.html', context)

def is_valid_queryparam(param):
    return param != '' and param is not None

#invoice list
def invoice_list(request):
    qs = Invoice.objects.order_by('-id')

    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    invoice_number = request.GET.get('invoice_number')
    client = request.GET.get('client')

    request.session['date_min'] = date_min
    request.session['date_max'] = date_max
    request.session['invoice_number'] = invoice_number
    request.session['client'] = client


    if is_valid_queryparam(invoice_number):
        qs = qs.filter(id__icontains=invoice_number)

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if is_valid_queryparam(client):
        qs = qs.filter(client__icontains=client)

    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 30)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'invoice_list': qs,
        'client': client,
        'invoice_number':invoice_number,
        'date_max':date_max,
        'date_min':date_min,
    }
    return render(request, "invoice/invoice_list.html", context)
