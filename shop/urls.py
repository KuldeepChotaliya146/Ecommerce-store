from django.contrib import admin
from django.urls import path,include
from shop import views
urlpatterns = [
    path('',views.product,name='product'),
    path('signup/',views.signupuser,name='signup'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkoutuser,name='checkout'),
    path('orders/',views.yourorder,name='yourorder'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
]

