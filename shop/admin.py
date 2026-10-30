from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Purchase


class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 0
    readonly_fields = ("amount", "points_earned", "created_at")
    can_delete = False


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("phone", "points", "created_at")
    search_fields = ("phone",)
    inlines = [PurchaseInline]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("customer", "amount", "points_earned", "created_at")
    list_filter = ("created_at",)
    search_fields = ("customer__phone",)