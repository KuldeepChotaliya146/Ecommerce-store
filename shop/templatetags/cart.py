from django import template
#register decorator
register = template.Library()
@register.filter(name='is_in_cart')
def is_in_cart(prd,cart):
    keys = cart.keys()
    for id in keys:
        #print(id,prd.id)
        #print(type(id),type(prd.id))
        if id == str(prd.id):
            return True
    return False

@register.filter(name='cart_count')
def cart_count(prd,cart):
    keys = cart.keys()
    for id in keys:
        #print(id,prd.id)
        #print(type(id),type(prd.id))
        if id == str(prd.id):
            return cart.get(id)
    return 0


@register.filter(name='price_total')
def price_total(prd,cart):
   return prd.price * cart_count(prd,cart)

@register.filter(name='total_cart_price')
def total_cart_price(prd,cart):
    sum = 0
    for i in prd:
        sum += price_total(i,cart)
    return sum

@register.filter(name='multilpy')
def multilpy(number,number1):
    return number*number1