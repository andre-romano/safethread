import unittest

# Adjust the import path as needed
from safethread.utils import Factory


# Sample subclass to test Factory behavior
class Product(Factory):
    def __init__(self, name: str, price: float):
        super().__init__()
        self.name = name
        self.price = price


# Sample subclass to test Factory behavior
class Object(Factory):
    def __init__(self):
        super().__init__()
        self.name = 'object'

    def setName(self, name):
        self.name = name


class TestFactory(unittest.TestCase):
    def setUp(self):
        """Setup method to run before each test."""
        self.product1 = Product.create("Widget", 19.99)
        self.product2 = Product.create("Widget A", 29.99)
        self.product3 = Product.create("Widget B", 39.99)
        self.product4 = Product.create("Gadget", 49.99)

        self.object = Object.create()

    def test_factory_create_instance(self):
        """Test that the Factory creates an instance of the subclass."""

        # Check that the created object is an instance of Product
        self.assertIsInstance(
            self.product1, Product, "Factory did not create an instance of the correct class")
        self.assertIsInstance(
            self.object, Object, "Factory did not create an instance of the correct class")

        # Check that the attributes are set correctly
        self.assertTrue(self.product1.name == "Widget",
                        "Product name was not set correctly by the factory")
        self.assertTrue(self.product1.price == 19.99,
                        "Product price was not set correctly by the factory")

    def test_factory_different_instances(self):
        """Test that the Factory creates different instances each time."""
        # Check that the two instances are different objects
        self.assertIsNot(
            self.product2, self.product3, "Factory returned the same instance instead of creating a new one")

        # Check that the attributes are set correctly for each instance
        self.assertTrue(self.product2.name != self.product3.name,
                        "Product names should be different")
        self.assertTrue(self.product2.price != self.product3.price,
                        "Product prices should be different")

    def test_factory_set_name(self):
        """Test that the arguments are passed correctly to the created object."""

        # Verify that the arguments were passed correctly
        self.assertTrue(self.object.name == "object",
                        "Object name not correct")

        self.object.setName('test')
        self.assertTrue(self.object.name == "test",
                        "Object name not correct")


if __name__ == '__main__':
    unittest.main()
