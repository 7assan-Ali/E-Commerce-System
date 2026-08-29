from src.models.product import Product
from src.models.customer import Customer


def test_cart_total():
    customer = Customer(1, "Hassan", "hassan@example.com", "1234", "01000000000", 1)
    product = Product(1, "Laptop", "Test laptop", 1000, 5, "LAP-001")
    customer.add_to_cart(product, 2)
    assert customer.cart.get_total() == 2000
