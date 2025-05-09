from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Product, Cart, CartItem
from ..serializers import CartSerializer, CartItemSerializer, ProductSerializer


class CartViewSet(ModelViewSet):
    @action(detail=False, methods=["post"], url_path="add-product/<product_id>/")
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
            if created:
                cart_item.amount = 1
            else:
                cart_item.amount += 1
            cart_item.save()
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default = {})
            cart[str(product_id)] = cart.get(str(product_id), default=0) + 1
        return Response(
            {
                "message" : f"Product with id #{product_id} was added to cart",
            }, status = 200
        )
    
    @action(detail=False, methods=['get'], url_path="get-cart-items/")
    def detail(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            # cart_items = cart.items.select_related("product").all()
            # data = [CartItemSerializer(item).data for item in cart_items]
            return Response(
                CartSerializer(cart).data
            )
        else:
            cart = request.session.get(
                settings.CART_SESSION_ID, default = {}
                )
            products = Product.objects.filter(id__in=cart.keys())
            items = []
            total = 0
            for product in products:
                data = ProductSerializer(product).data
                amount = cart.get(str(product.id))
                item_total = (product.discount_price or product.price) * amount
                items.append(
                    "product":data
                )