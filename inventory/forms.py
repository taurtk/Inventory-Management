from django import forms
from django.core.validators import RegexValidator
from .models import Product, Supplier, SaleOrder, StockMovement,Category

# Add to e

class SupplierForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be 10 digits'
            )
        ]
    )

    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter supplier name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter 10-digit phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Enter complete address'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Supplier.objects.filter(email=email).exists():
            raise forms.ValidationError('A supplier with this email already exists.')
        return email

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'supplier']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'min': '1',
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')

        if product and quantity:
            if quantity > product.stock_quantity:
                raise forms.ValidationError(
                    f"Insufficient stock. Only {product.stock_quantity} units available."
                )
        return cleaned_data


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select rounded-lg border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200',
            }),
            'movement_type': forms.Select(attrs={
                'class': 'form-select rounded-lg border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input rounded-lg border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200',
                'min': '1',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea rounded-lg border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200',
                'rows': '3',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        movement_type = cleaned_data.get('movement_type')
        quantity = cleaned_data.get('quantity')

        if product and movement_type and quantity:
            if movement_type == 'OUT' and quantity > product.stock:
                raise forms.ValidationError(
                    f"Cannot remove {quantity} units. Only {product.stock} units available in stock."
                )

        return cleaned_data