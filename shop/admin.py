from django.contrib import admin
from .models import *
# Register your models here.
class Adminproduct(admin.ModelAdmin):
    list_display = ['id','name','price','category']

class Admincategory(admin.ModelAdmin):
    list_display = ['name']

class Admincustomer(admin.ModelAdmin):
    list_display = ['id','firstname','lastname','email','phoneno']



admin.site.register(Product,Adminproduct)
admin.site.register(Category,Admincategory)
admin.site.register(Customer,Admincustomer)
admin.site.register(Order)