from rest_framework import viewsets, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Customer, Invoice, InvoiceItem 
from .serializers import CustomerSerializer, InvoiceSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class InvoiceViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user).prefetch_related('items')
        return Invoice.objects.none()

    def perform_create(self, serializer):
        
        items_data = self.request.data.get('items', [])
        
        
        invoice = serializer.save(user=self.request.user)
                                
        
        for item in items_data:
            InvoiceItem.objects.create(
                invoice=invoice,
                product_name=item.get('product_name'),
                quantity=item.get('quantity', 1),
                price=item.get('price', 0)
            )


@api_view(['POST'])
@permission_classes([AllowAny])  # anyone can register
def register_user(request):
    data = request.data

    try:
        
        if User.objects.filter(username=data.get('username')).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email', '')
        )

        return Response(
            {'message': 'User created successfully'},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )