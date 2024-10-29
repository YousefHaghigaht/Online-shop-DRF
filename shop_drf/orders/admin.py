from django.contrib import admin
from .models import Order,OrderItem,Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('products',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','paid')
    list_filter = ('paid',)
    ordering = ('paid','created')
    inlines = (OrderItemInline,)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','discount')


