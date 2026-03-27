from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    
   
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    
    date_created = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year = datetime.datetime.now().year
            # Corrected order_by here
            last_invoice = Invoice.objects.filter(
                invoice_number__contains=f'INV-{year}'
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                last_no = int(last_invoice.invoice_number.split('-')[-1])
                new_no = f"{last_no + 1:03d}"
            else:
                new_no = "001"
            
            self.invoice_number = f'INV-{year}-{new_no}'
        
        super(Invoice, self).save(*args, **kwargs)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_name} ({self.quantity})"