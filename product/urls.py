from django.urls import path
from product import views

urlpatterns = [
    path('shop_category/', views.shop_category,name='shop_category'),
    path('product/', views.product,name='product'),
    path('add_seller/', views.add_seller,name='add_seller'),
    path('seller_select_category/<int:id>', views.seller_select_category,name='seller_select_category'),
    path('select_seller_cat', views.select_seller_cat,name='select_seller_cat'),
    path('seller_product/', views.seller_product,name='seller_product'),
    path('add_product/', views.add_product,name='add_product'),
    path('edit_product/<int:id>', views.edit_product,name='edit_product'),
    path('select_prd_cat', views.select_prd_cat,name='select_prd_cat'),
    path('product_select_category/<int:id>', views.product_select_category,name='product_select_category'),

]