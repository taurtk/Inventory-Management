from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Product, Supplier, SaleOrder, StockMovement
from .forms import ProductForm, SupplierForm, SaleOrderForm, StockMovementForm
from .filters import ProductFilter, SaleOrderFilter, StockMovementFilter
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import StockMovement
from .forms import StockMovementForm 
from django.contrib.auth.decorators import login_required

def home(request):
    return redirect('inventory:product_list')

# Update the product_list view
def product_list(request):
    product_filter = ProductFilter(
        request.GET,
        queryset=Product.objects.select_related('supplier').all()
    )
    
    paginator = Paginator(product_filter.qs, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'inventory/product_list.html', {
        'filter': product_filter,
        'products': products
    })
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/add_supplier.html', {'form': form})


# Update the sale_order_list view
def sale_order_list(request):
    sale_filter = SaleOrderFilter(
        request.GET,
        queryset=SaleOrder.objects.select_related('product').all()
    )
    
    paginator = Paginator(sale_filter.qs, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    return render(request, 'inventory/sale_order_list.html', {
        'filter': sale_filter,
        'orders': orders
    })
@transaction.atomic
def create_sale_order(request):
    if request.method == 'POST':
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            sale_order = form.save(commit=False)
            product = sale_order.product
            quantity = sale_order.quantity
            
            # Calculate total price
            sale_order.total_price = product.price * quantity
            sale_order.save()

            # Create stock movement
            StockMovement.objects.create(
                product=product,
                quantity=quantity,
                movement_type='OUT',
                notes=f'Sale order #{sale_order.id}'
            )

            # Update product stock
            product.stock_quantity -= quantity
            product.save()

            messages.success(request, 'Sale order created successfully!')
            return redirect('inventory:sale_order_list')
    else:
        form = SaleOrderForm()
    
    return render(request, 'inventory/create_sale_order.html', {'form': form})

@transaction.atomic
def cancel_sale_order(request, order_id):
    order = get_object_or_404(SaleOrder, id=order_id)
    
    if order.status == 'CANCELLED':
        messages.error(request, 'This order is already cancelled.')
        return redirect('sale_order_list')
    
    if order.status == 'COMPLETED':
        messages.error(request, 'Cannot cancel a completed order.')
        return redirect('sale_order_list')

    # Return stock to inventory
    product = order.product
    product.stock_quantity += order.quantity
    product.save()

    # Create stock movement
    StockMovement.objects.create(
        product=product,
        quantity=order.quantity,
        movement_type='IN',
        notes=f'Cancelled sale order #{order.id}'
    )

    # Update order status
    order.status = 'CANCELLED'
    order.save()

    messages.success(request, 'Sale order cancelled successfully!')
    return redirect('sale_order_list')

@transaction.atomic
def complete_sale_order(request, order_id):
    order = get_object_or_404(SaleOrder, id=order_id)
    
    if order.status != 'PENDING':
        messages.error(request, f'Cannot complete {order.status.lower()} order.')
        return redirect('inventory:sale_order_list')

    order.status = 'COMPLETED'
    order.save()

    messages.success(request, 'Sale order completed successfully!')
    return redirect('inventory:sale_order_list')


# Add to existing views.py

# Update the stock_movement_list view
def stock_movement_list(request):
    movement_filter = StockMovementFilter(
        request.GET,
        queryset=StockMovement.objects.select_related('product').all()
    )
    
    paginator = Paginator(movement_filter.qs, 10)
    page_number = request.GET.get('page')
    movements = paginator.get_page(page_number)
    
    return render(request, 'inventory/stock_movement_list.html', {
        'filter': movement_filter,
        'movements': movements
    })

@login_required
def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            stock_movement = form.save(commit=False)
            stock_movement.created_by = request.user
            stock_movement.save()
            
            # Update product stock
            product = stock_movement.product
            if stock_movement.movement_type == 'IN':
                product.stock_quantity += stock_movement.quantity
            else:
                product.stock_quantity -= stock_movement.quantity
            product.save()
            
            messages.success(request, 'Stock movement recorded successfully.')
            return redirect('inventory:stock_movement_list')
    else:
        form = StockMovementForm()
    
    return render(request, 'inventory/stock_movement_form.html', {
        'form': form,
        'title': 'Add Stock Movement'
    })


def check_stock_levels(request):
    products = Product.objects.select_related('supplier').all()
    low_stock_threshold = 10  # You can make this configurable
    
    for product in products:
        product.low_stock = product.stock_quantity <= low_stock_threshold
        
    return render(request, 'inventory/stock_levels.html', {
        'products': products,
        'low_stock_threshold': low_stock_threshold
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def stock_levels(request):
    products = Product.objects.select_related('category', 'supplier').all()
    
    context = {
        'products': products,
        'title': 'Stock Levels'
    }
    
    return render(request, 'inventory/stock_levels.html', context)