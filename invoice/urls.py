from django.urls import path, include
from . import views 

urlpatterns = [
	path('create_invoice', views.create_invoice, name='create_invoice'),
	path('', views.invoice_list, name='invoice_list'),
	path('<int:pk>/add_item_invoice', views.add_item_invoice, name='add_item_invoice'),
	path('<int:pk>/invoicepdf', views.invoicepdf, name='invoicepdf'),
	path('<int:pk>/invoice_detail', views.invoice_detail, name='invoice_detail'),
	path('<int:pk>/invoice_payment', views.invoice_payment, name='invoice_payment'),
	]