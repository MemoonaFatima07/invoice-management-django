from rest_framework import serializers
from .models import Customer, Invoice, InvoiceItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = InvoiceItem
        fields = ['id', 'product_name', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()

class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    items = InvoiceItemSerializer(many=True)
    total = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True) # Automatically handled

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'user', 'customer', 'customer_name', 'status', 'items', 'total', 'date_created', 'due_date']

    def get_total(self, obj):
        return float(obj.get_total())
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice