from django.urls import path
from sunil import views


urlpatterns = [
    path('sunil_login/', views.sunil_login,name='sunil_login'),
    path('add_admin/', views.add_admin,name='add_admin'),
    path('admin_logout/', views.admin_logout,name='admin_logout'),
    path('admin_dashboard/', views.admin_dashboard,name='admin_dashboard'),
    
]