# urls.py

from django.urls import path
from .views import checkout, update_order_status,order_confirmation

app_name = 'checkout'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
]
