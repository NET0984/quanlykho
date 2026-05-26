from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # --- TRANG 1: QUẢN LÝ SẢN PHẨM ---
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<uuid:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<uuid:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<uuid:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # --- TRANG 2: QUẢN LÝ DANH MỤC ---
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<uuid:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<uuid:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # --- TRANG 3: QUẢN LÝ ĐƠN VỊ & QUY ĐỔI ---
    path('units/', views.ProductUnitListView.as_view(), name='units_list'), 
    path('unit/add/', views.ProductUnitCreateView.as_view(), name='unit_add'),
    path('unit/<uuid:pk>/update/', views.ProductUnitUpdateView.as_view(), name='unit_update'),
    path('unit/<uuid:pk>/delete/', views.ProductUnitDeleteView.as_view(), name='unit_delete'),
]