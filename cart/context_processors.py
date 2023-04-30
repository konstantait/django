from cart.cart import Cart
from core.settings import CART_SESSION_ID


def cart(request):
    return {CART_SESSION_ID: Cart(request)}
