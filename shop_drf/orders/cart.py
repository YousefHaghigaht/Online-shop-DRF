from products.models import Product

CART_SESSION_ID = 'cart'


class Cart():

    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        products_id = self.cart.keys()
        products = Product.objects.filter(id__in=products_id)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = item['quantity'] * item['price']
            yield item

    def add(self,quantity,product):
        product_id = str(product.id)
        if not product_id in self.cart:
            self.cart[product_id] = {'quantity':0 , 'price':str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def delete(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
