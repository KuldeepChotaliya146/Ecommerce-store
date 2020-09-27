from django.db import models
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_cat():
        return Category.objects.all()
       
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=100,default='')
    image = models.ImageField(upload_to='products/images/')

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_by_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    @staticmethod
    def addcart(ids):
        return Product.objects.filter(id__in=ids)

class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phoneno = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname
    def isExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False
    @staticmethod
    def getcustomer(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False
            
    
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    status = models.BooleanField(default=0)
    address = models.CharField(max_length=100,default='Navsari')
    phone = models.CharField(max_length=15,default=9484649914)
    date = models.DateField(default=datetime.datetime.today)


    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(Customer=customer_id)

    
    
    


    