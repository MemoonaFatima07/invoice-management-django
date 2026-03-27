from django.contrib import admin
from .models import Invoice, InvoiceItem, Customer


# Inline for invoice items
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


# Invoice admin
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ( 'invoice_number','id', 'customer', 'date_created','due_date' ,'status', 'show_total')
    list_filter = ('status', 'date_created')
    inlines = [InvoiceItemInline]


    def show_total(self, obj):
        return obj.total_amount()


# Customer admin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


# Register models
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Customer, CustomerAdmin)