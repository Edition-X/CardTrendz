import unittest
from unittest import mock
from main import _get_start_block
from datetime import datetime, timedelta
import pytz

# Define a fixed time for the datetime.now() to return during the tests
_fixed_time = datetime(2023, 7, 30, 12, 0, 0, 0, tzinfo=pytz.UTC)

# Create a mock for datetime that will return _fixed_time when now() is called
class MockDateTime:
    @classmethod
    def now(cls, tz):
        return _fixed_time

class TestGetStartBlock(unittest.TestCase):
    @mock.patch('main.Blockchain')
    @mock.patch('main.datetime', new=MockDateTime)
    def test_get_start_block_days(self, MockBlockchain):
        # Given
        mock_blockchain = MockBlockchain()
        time_unit = "days"
        time_amount = 3
        x_time_ago = _fixed_time - timedelta(days=time_amount)
        mock_blockchain.get_estimated_block_num.return_value = 123456
        # When
        result = _get_start_block(mock_blockchain, time_unit, time_amount)
        # Then
        mock_blockchain.get_estimated_block_num.assert_called_once_with(x_time_ago)
        self.assertEqual(result, 123456)

    @mock.patch('main.Blockchain')
    @mock.patch('main.datetime', new=MockDateTime)
    def test_get_start_block_hours(self, MockBlockchain):
        # Given
        mock_blockchain = MockBlockchain()
        time_unit = "hours"
        time_amount = 12
        x_time_ago = _fixed_time - timedelta(hours=time_amount)
        mock_blockchain.get_estimated_block_num.return_value = 654321
        # When
        result = _get_start_block(mock_blockchain, time_unit, time_amount)
        # Then
        mock_blockchain.get_estimated_block_num.assert_called_once_with(x_time_ago)
        self.assertEqual(result, 654321)

    @mock.patch('main.Blockchain')
    def test_get_start_block_invalid_unit(self, MockBlockchain):
        # Given
        mock_blockchain = MockBlockchain()
        time_unit = "invalid"
        time_amount = 12
        # When
        result = _get_start_block(mock_blockchain, time_unit, time_amount)
        # Then
        mock_blockchain.get_estimated_block_num.assert_not_called()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

