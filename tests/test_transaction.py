import unittest
from unittest import mock
from main import _check_transaction_success, _store_purchase_data

class TestCheckTransactionSuccess(unittest.TestCase):
    @mock.patch('main.Api')
    def test_check_transaction_success_successful(self, MockApi):
        # Given
        mock_api = MockApi()
        trx_id = "test_trx_id"
        card_data = set()
        mock_response = {"trx_info": {"success": True, "data": '{"cards": ["C3-134-32H0Y04KHC"], "price": 5.17275}', "created_date": "2023-07-28T04:26:21.000Z", "id": "7ad14568086a03b30f496646d616a9013f980db9"}}
        mock_api.get_transaction.return_value = mock_response
        expected_data = _store_purchase_data(mock_response['trx_info'], set())
        # When
        success, result = _check_transaction_success(trx_id, card_data)
        # Then
        self.assertTrue(success)
        self.assertEqual(result, expected_data)

    @mock.patch('main.Api')
    def test_check_transaction_success_unsuccessful(self, MockApi):
        # Given
        mock_api = MockApi()
        trx_id = "test_trx_id"
        card_data = set()
        mock_response = {"trx_info": {"success": False, "data": '{"cards": ["C3-134-32H0Y04KHC"], "price": 5.17275}', "created_date": "2023-07-28T04:26:21.000Z", "id": "7ad14568086a03b30f496646d616a9013f980db9"}}
        mock_api.get_transaction.return_value = mock_response
        # When
        success, result = _check_transaction_success(trx_id, card_data)
        # Then
        self.assertFalse(success)
        self.assertEqual(result, card_data)

    @mock.patch('main.Api')
    def test_check_transaction_success_no_trx_info(self, MockApi):
        # Given
        mock_api = MockApi()
        trx_id = "test_trx_id"
        card_data = set()
        mock_response = {}
        mock_api.get_transaction.return_value = mock_response
        # When
        success, result = _check_transaction_success(trx_id, card_data)
        # Then
        self.assertFalse(success)
        self.assertEqual(result, card_data)
