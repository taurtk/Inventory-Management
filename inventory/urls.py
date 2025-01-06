from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('sales/', views.sale_order_list, name='sale_order_list'),
    path('sales/create/', views.create_sale_order, name='create_sale_order'),
    path('sales/<int:order_id>/cancel/', views.cancel_sale_order, name='cancel_sale_order'),
    path('sales/<int:order_id>/complete/', views.complete_sale_order, name='complete_sale_order'),
    path('stock/', views.stock_movement_list, name='stock_movement_list'),
    path('stock/add/', views.add_stock_movement, name='add_stock_movement'),
    path('stock/levels/', views.stock_levels, name='stock_levels'),
]