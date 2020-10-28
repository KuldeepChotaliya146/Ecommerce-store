from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum
# Create your views here.

merchant_key = 'XiXbHrjTeTKkpEv3'
def product(request):
    if request.method == "GET":
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        categories = Category.get_all_cat()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_by_id(categoryID)
        else:
            products = Product.get_all_products()
        return render(request, 'products.html', {'products': products, 'categories': categories})
    else:
        product = request.POST.get('product')
        remove = request.POST.get('minus')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        # print(request.session['cart'])
        return redirect('product')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phoneno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        values = {
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'phoneno': phone,
        }
        error_msg = None
        customer = Customer(firstname=first_name, lastname=last_name,
                            phoneno=phone, email=email, password=password)
        # validation
        if len(phone) > 10:
            error_msg = "Phone number should be less than 10"
        elif (password != repassword):
            error_msg = "Password is not same"
        elif (len(password) and len(repassword)) < 8:
            error_msg = "Password length must be 8."
        elif customer.isExist():
            error_msg = "Email Already exists..."

        if not error_msg:
            customer.password = make_password(customer.password)
            request.session['customer'] = customer.id
            request.session['email'] = customer.email
            customer.save()
            return redirect('login')
        else:
            return render(request, 'signup.html', {'error': error_msg, 'value': values})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        customer = Customer.getcustomer(email)
        error_msg = None
        if customer:
            valid = check_password(pwd, customer.password)
            if valid:
                request.session['customer'] = customer.id
                return HttpResponseRedirect('/')
            else:
                error_msg = "Email or Password not valid..!"
        else:
            error_msg = "Email or Password not valid..!"
        return render(request, 'login.html', {'error': error_msg})


def logoutuser(request):
    request.session.clear()
    return redirect('login')


def cart(request):
    if request.method == 'GET':
        ids = list(request.session.get('cart').keys())
        products = Product.addcart(ids)
        return render(request, 'cart.html', {'products': products})


def checkoutuser(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        amount = request.POST.get('amount')
        cart = request.session.get('cart')
        # print(cart)
        products = Product.addcart(list(cart.keys()))
        for product in products:
            order = Order(Customer=Customer(id=customer), product=product, price=product.price,
                          address=address, phone=phone, quantity=cart.get(str(product.id)))
            order.save()
        param_dict={

            'MID': 'SWLdgW39069691289143',
            'ORDER_ID': str(order.id),
            'TXN_AMOUNT': amount,
            'CUST_ID': str(phone),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,merchant_key)
        return render(request,'paytm.html',{'param_dict':param_dict})

    return redirect('cart')

@csrf_exempt
def handlerequest(request):
    return HttpResponse("Done")



def yourorder(request):
    if request.method == "GET":
        customer = request.session.get('customer')
        order = Order.get_orders_by_customer(customer)
        return render(request, 'orders.html', {'order': order})



