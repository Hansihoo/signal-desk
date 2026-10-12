import http.client
import json
import threading
import unittest
from http.server import HTTPServer
from app import Handler
from sorting import sort_products


class SortingTests(unittest.TestCase):
    def test_numeric_order(self):
        products = [{'id': 'a', 'price': 10}, {'id': 'b', 'price': 2}, {'id': 'c', 'price': 1}]
        self.assertEqual([p['price'] for p in sort_products(products)], [1, 2, 10])

    def test_empty(self):
        self.assertEqual(sort_products([]), [])

    def test_single(self):
        products = [{'id': 'a', 'price': 2}]
        self.assertEqual(sort_products(products), products)

    def test_equal_prices_keep_order(self):
        products = [{'id': 'a', 'price': 2}, {'id': 'b', 'price': 2}]
        self.assertEqual([p['id'] for p in sort_products(products)], ['a', 'b'])

    def test_does_not_reorder_input(self):
        products = [{'id': 'a', 'price': 10}, {'id': 'b', 'price': 2}]
        sort_products(products)
        self.assertEqual([p['id'] for p in products], ['a', 'b'])

    def test_missing_price(self):
        with self.assertRaises(ValueError):
            sort_products([{'id': 'a'}])

    def test_invalid_price(self):
        for price in ['2', -1, True, 2.5]:
            with self.subTest(price=price), self.assertRaises(ValueError):
                sort_products([{'id': 'a', 'price': price}])

    def test_invalid_shape(self):
        for products in [None, {}, ['a'], [{'price': 1}]]:
            with self.subTest(products=products), self.assertRaises(ValueError):
                sort_products(products)


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def request(self, method, path, body=None):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=5)
        try:
            connection.request(method, path, body=body, headers={'Content-Type': 'application/json'})
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def test_health(self):
        status, data = self.request('GET', '/health')
        self.assertEqual((status, data['status'], data['version']), (200, 'ok', 'local'))

    def test_sort_request(self):
        body = json.dumps({'products': [{'id': 'a', 'price': 10}, {'id': 'b', 'price': 2}]})
        status, data = self.request('POST', '/sort', body)
        self.assertEqual(status, 200)
        self.assertEqual([p['id'] for p in data['products']], ['b', 'a'])

    def test_missing_price_request(self):
        status, data = self.request('POST', '/sort', '{"products":[{"id":"a"}]}')
        self.assertEqual(status, 400)
        self.assertIn('price', data['error'])

    def test_bad_json_request(self):
        status, data = self.request('POST', '/sort', '{')
        self.assertEqual(status, 400)
        self.assertIn('error', data)
