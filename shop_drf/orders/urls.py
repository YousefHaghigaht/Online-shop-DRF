from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('create/',views.OrderCreate.as_view(), name='create'),
    path('detail/<int:order_id>/',views.OrderDetailView.as_view(),name='detail'),
    path('api/payment/',views.ZarinPalPaymentView.as_view(), name='zarinpal_payment'),
]
