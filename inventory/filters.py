import django_filters
from django import forms
from .models import Product, SaleOrder, StockMovement

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    category = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    supplier = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'supplier']

class SaleOrderFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_date = django_filters.DateFilter(
        field_name='sale_date',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    max_date = django_filters.DateFilter(
        field_name='sale_date',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    status = django_filters.ChoiceFilter(
        choices=SaleOrder.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SaleOrder
        fields = ['product', 'status']

class StockMovementFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    movement_type = django_filters.ChoiceFilter(
        choices=StockMovement.MOVEMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    max_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'created_at']