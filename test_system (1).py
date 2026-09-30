import unittest
from unittest.mock import patch
from io import StringIO

import main


class TestSettlementAgent(unittest.TestCase):

    def test_successful_transaction(self):
        with patch("sys.stdout", new=StringIO()) as output:
            main.trace_transaction("TXN1001")

        result = output.getvalue()

        self.assertIn("Settlement completed successfully.", result)
        self.assertIn("SETTLED", result)
        self.assertIn("RECORDED", result)

    def test_pending_transaction(self):
        with patch("sys.stdout", new=StringIO()) as output:
            main.trace_transaction("TXN1002")

        result = output.getvalue()

        self.assertIn("Settlement requires attention.", result)
        self.assertIn("Bank settlement is still pending.", result)

    def test_failed_transaction(self):
        with patch("sys.stdout", new=StringIO()) as output:
            main.trace_transaction("TXN1003")

        result = output.getvalue()

        self.assertIn("Settlement requires attention.", result)
        self.assertIn("Gateway did not process the transaction.", result)
        self.assertIn("Bank did not receive the transaction.", result)
        self.assertIn(
            "Transaction is not recorded in the ledger.",
            result
        )

    def test_invalid_transaction(self):
        with patch("sys.stdout", new=StringIO()) as output:
            main.trace_transaction("TXN9999")

        result = output.getvalue()

        self.assertIn("Transaction ID not found.", result)

    def test_date_search(self):
        with patch("sys.stdout", new=StringIO()) as output:
            main.search_by_date("2026-09-20")

        result = output.getvalue()

        self.assertIn("TXN1001", result)
        self.assertIn("TXN1002", result)

    def test_date_with_no_transactions(self):
        with patch("sys.stdout", new=StringIO()) as output:
            main.search_by_date("2026-10-01")

        result = output.getvalue()

        self.assertIn("No transactions found for this date.", result)


if __name__ == "__main__":
    unittest.main()