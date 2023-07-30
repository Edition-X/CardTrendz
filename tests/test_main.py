import unittest
from main import _store_purchase_data

class TestScript(unittest.TestCase):

    def test_store_purchase_data_with_list(self):
        card_data = set()
        # Prepare data
        trx_info = {"data": '[{"cards": ["C3-134-32H0Y04KHC"], "price": 5.17275}]', "created_date": "2023-07-28T04:26:21.000Z", "id": "7ad14568086a03b30f496646d616a9013f980db9"}
        # Expected result
        expected = {(('card_uid', ('C3-134-32H0Y04KHC',)), ('created_date', '2023-07-28T04:26:21.000Z'), ('price', 5.17275), ('trx_id', '7ad14568086a03b30f496646d616a9013f980db9'))}
        # Call function
        _store_purchase_data(trx_info, card_data)
        # Check result
        self.assertEqual(card_data, expected)

    def test_store_purchase_data_with_dict(self):
        card_data = set()
        # Prepare data
        trx_info = {"data": '{"cards": ["C3-134-32H0Y04KHC"], "price": 5.17275}', "created_date": "2023-07-28T04:26:21.000Z", "id": "7ad14568086a03b30f496646d616a9013f980db9"}
        # Expected result
        expected = {(('card_uid', ('C3-134-32H0Y04KHC',)), ('created_date', '2023-07-28T04:26:21.000Z'), ('price', 5.17275), ('trx_id', '7ad14568086a03b30f496646d616a9013f980db9'))}
        # Call function
        _store_purchase_data(trx_info, card_data)
        # Check result
        self.assertEqual(card_data, expected)

    def test_store_purchase_data_no_cards(self):
        card_data = set()
        # Prepare data
        trx_info = {"data": '{"items": "C3-134-32H0Y04KHC", "price": 5.17275}', "created_date": "2023-07-28T04:26:21.000Z", "id": "7ad14568086a03b30f496646d616a9013f980db9"}
        # Expected result
        expected = set()
        # Call function
        _store_purchase_data(trx_info, card_data)
        # Check result
        self.assertEqual(card_data, expected)

if __name__ == '__main__':
    unittest.main()

