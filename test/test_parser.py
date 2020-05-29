import os
import unittest

from pdfminer import high_level

from app.helpers.parser import OrderItem, Order


class TestParser(unittest.TestCase):
    def setUp(self):
        self.test_order_id_1 = '140-2475861-372856'
        self.test_order_id_2 = '214-2871494-7469807'
        self.test_order_date_placed_1 = 'February 25, 2017'
        self.test_order_date_placed_2 = 'April 27, 2020'
        self.test_order_order_total_1 = 109.33
        self.test_order_order_total_2 = 200.00
        self.test_order_date_shipped_1 = 'February 16, 2017'
        self.test_order_date_shipped_2 = self.test_order_date_placed_2
        self.test_order_shipping_loc_1 = {
            'City': 'London',
            'Region': 'England',
            'PostalCode': '27475',
            'Country': 'United Kingdom'
        }
        self.test_order_shipping_loc_2 = {}
        self.test_order_shipping_speed_1 = 'Standard Shipping'
        self.test_order_shipping_speed_2 = ''
        self.test_order_payment_method = 'Visa'
        self.test_order_billing_loc_1 = self.test_order_shipping_loc_1
        self.test_order_billing_loc_2 = {
            'City': 'Little Whinging',
            'Region': 'Surrey',
            'PostalCode': '5UK8',
            'Country': 'England'
        }
        self.test_item_name_1 = "AmazonBasics Wand"
        self.test_item_name_2 = "Gift card"
        self.test_item_quantity = 1
        self.test_item_price_1 = 108.00
        self.test_item_price_2 = 100.00
        self.test_item_sold_by = "Amazon.com Services LLC"
        self.test_item_condition = "New"
        self.test_order_item_1 = OrderItem(self.test_item_name_1, self.test_item_quantity, self.test_item_price_1,
                                           self.test_item_sold_by, self.test_item_condition)
        self.test_order_item_2 = OrderItem(self.test_item_name_2, self.test_item_quantity, self.test_item_price_2,
                                           self.test_item_sold_by, self.test_item_condition)
        self.test_order_items_1 = [self.test_order_item_1]
        self.test_order_items_2 = [self.test_order_item_2, self.test_order_item_2]
        self.test_pdf_1 = f'test{os.sep}example1.pdf'
        self.test_pdf_2 = f'test{os.sep}example2.pdf'

    def test_pdf_1_order_is_expected(self):
        lines = high_level.extract_text(self.test_pdf_1).splitlines(keepends=False)
        order = Order(lines)
        self.assertEqual(order.id, self.test_order_id_1)
        self.assertEqual(order.date_placed, self.test_order_date_placed_1)
        self.assertEqual(order.order_total, self.test_order_order_total_1)
        self.assertListEqual(order.items, self.test_order_items_1)
        self.assertEqual(order.date_shipped, self.test_order_date_shipped_1)
        self.assertEqual(order.shipping_loc, self.test_order_shipping_loc_1)
        self.assertEqual(order.shipping_speed, self.test_order_shipping_speed_1)
        self.assertEqual(order.payment_method, self.test_order_payment_method)
        self.assertEqual(order.billing_loc, self.test_order_billing_loc_1)

    def test_pdf_2_order_is_expected(self):
        lines = high_level.extract_text(self.test_pdf_2).splitlines(keepends=False)
        order = Order(lines)
        self.assertEqual(order.id, self.test_order_id_2)
        self.assertEqual(order.date_placed, self.test_order_date_placed_2)
        self.assertEqual(order.order_total, self.test_order_order_total_2)
        self.assertListEqual(order.items, self.test_order_items_2)
        self.assertEqual(order.date_shipped, self.test_order_date_shipped_2)
        self.assertEqual(order.shipping_loc, self.test_order_shipping_loc_2)
        self.assertEqual(order.shipping_speed, self.test_order_shipping_speed_2)
        self.assertEqual(order.payment_method, self.test_order_payment_method)
        self.assertEqual(order.billing_loc, self.test_order_billing_loc_2)

    def test_pdf_1_order_item_is_expected(self):
        lines = high_level.extract_text(self.test_pdf_1).splitlines(keepends=False)
        self.assertEqual(Order(lines).items[0], self.test_order_item_1)

    def test_pdf_2_order_items_are_expected(self):
        lines = high_level.extract_text(self.test_pdf_2).splitlines(keepends=False)
        order = Order(lines)
        self.assertEqual(order.items[0], self.test_order_item_2)
        self.assertEqual(order.items[1], self.test_order_item_2)


if __name__ == '__main__':
    unittest.main()
