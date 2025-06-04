import pytest

from products.models import Category, Product, Order



@pytest.fixture()
def category():
    return Category.objects.create(name='Category')

@pytest.fixture
def product():
    category = Category.objects.create(name="test-category")
    return Product.objects.create(
        name="test-product",
        category=category,
        nomenclature="test-nomenclature",
        price=100,
    )


@pytest.fixture
def product_discount():
    category = Category.objects.create(name="test-category_2")

    return Product.objects.create(
        name="test_product",
        category=category,
        nomenclature="test-nomenclature_2",
        price=100,
        discount=10,
    )


@pytest.fixture
def order(user):
    return Order.objects.create(
        user=user,
        contact_name="Test_contact_name_1",
        contact_email="Test_contact_email1@gmail.com",
        contact_phone="+00000001",
        address="Test_adress_field_1",
    )