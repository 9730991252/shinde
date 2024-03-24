from django.urls import path
from order import views
urlpatterns = [
    path('add_to_cart', views.add_to_cart,name='add_to_cart'),
    path('customer_mobile', views.customer_mobile,name='customer_mobile'),
    path('cart/', views.cart,name='cart'),
    path('pending_order/', views.pending_order,name='pending_order'),
    path('view_pending_order/<int:id>/', views.view_pending_order,name='view_pending_order'),
    

]