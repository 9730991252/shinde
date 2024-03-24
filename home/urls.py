from django.urls import path
from home import views


urlpatterns = [
    path('', views.index,name='index'),
    path('login/', views.login,name='login'),
    path('seller_dashboard/', views.seller_dashboard,name='seller_dashboard'),
    path('filter_product', views.filter_product,name='filter_product'),
    path('product_detail/<int:id>', views.product_detail,name='product_detail'),

    
    
    
]