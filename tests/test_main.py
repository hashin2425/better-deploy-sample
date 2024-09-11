import json
import unittest
import azure.functions as func

from unittest.mock import patch, mock_open
from main import main, load_database, find_product


class TestProductAPI(unittest.TestCase):

    def setUp(self):
        self.test_data = [{"id": 1, "name": "Product 1"}, {"id": 2, "name": "Product 2"}]

    def test_load_database(self):
        mock_file_data = json.dumps(self.test_data)
        with patch("builtins.open", mock_open(read_data=mock_file_data)):
            result = load_database("dummy_path")
        self.assertEqual(result, self.test_data)

    def test_find_product(self):
        product = find_product(self.test_data, 1)
        self.assertEqual(product, {"id": 1, "name": "Product 1"})

        product = find_product(self.test_data, 3)
        self.assertIsNone(product)

    @patch("main.load_database")
    def test_main_valid_id(self, mock_load_database):
        mock_load_database.return_value = self.test_data
        req = func.HttpRequest(method="GET", body=None, url="/api/func_return_html", params={"id": "1"})
        response = main(req)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_body()), {"id": 1, "name": "Product 1"})

    def test_main_invalid_id(self):
        req = func.HttpRequest(method="GET", body=None, url="/api/func_return_html", params={"id": "invalid"})
        response = main(req)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_body().decode(), "Invalid id")

    @patch("main.load_database")
    def test_main_product_not_found(self, mock_load_database):
        mock_load_database.return_value = self.test_data
        req = func.HttpRequest(method="GET", body=None, url="/api/func_return_html", params={"id": "3"})
        response = main(req)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_body().decode(), "Product not found")

    @patch("main.load_database")
    def test_main_internal_error(self, mock_load_database):
        mock_load_database.side_effect = Exception("Test exception")
        req = func.HttpRequest(method="GET", body=None, url="/api/func_return_html", params={"id": "1"})
        response = main(req)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(response.get_body().decode().startswith("Internal server error"))


if __name__ == "__main__":
    unittest.main()
