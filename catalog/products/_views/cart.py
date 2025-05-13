from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from django.shortcuts import get_object_or_404
from ..models import Cart, Product, CartItem
from ..serializers.cart_serializers import CartSerializer, CartItemSerializer
from ..serializers.product_serializers import ProductSerializer



@extend_schema_view(
    list=extend_schema(summary="Get Carts List"),
    create=extend_schema(summary="Create Cart"),
    update=extend_schema(summary="Update Cart"),
    partial_update=extend_schema(summary="Partial Update Cart"),
)


class CartViewSet(ViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @extend_schema(
        responses={200: CartSerializer},
        description="Add Product To Cart"
    )

    @action(detail=True, methods=["post"], url_path="add-product/<int:product_id>/")
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = request.user.cart
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
            if created:
                cart_item.amount = 1
            else:
                cart_item.amount += 1
            cart_item.save()
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            cart[str(product_id)] = cart.get(str(product_id), 0) + 1
            request.session[settings.CART_SESSION_ID] = cart  
        return Response({"message": f"Product with id {product_id} added"}, status=200)

    @extend_schema(
        responses={200: CartSerializer},
        description="Get Info"
    )
    @action(detail=False, methods=['get'], url_path="get-cart-items/")
    def detail(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            return Response(CartSerializer(cart).data)
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            if not cart:
                return Response({"message": "Your cart is empty."}, status=200)
            products = Product.objects.filter(id__in=cart.keys())
            items = []
            total = 0
            for product in products:
                data = ProductSerializer(product).data
                amount = cart.get(str(product.id))
                item_total = (product.discount_price or product.price) * amount
                items.append({
                    "product": data,
                    "amount": amount,
                    "item_total": item_total,
                    "cart": None,
                })
                total += item_total
            return Response({"user": request.user, "created_at": None, "items": items, "total": total})
