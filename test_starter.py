import unittest
from decimal import Decimal

from starter import recommend_price


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    async def test_calculates_price_from_eligible_offers(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "mYsHoP", "price": Decimal("4300.00"), "delivery_days": 2},
                    {"seller": "Конкурент", "price": Decimal("4800.01"), "delivery_days": 6},
                    {"seller": "Доставка неизвестна", "price": Decimal("4100.00"), "delivery_days": None},
                    {"seller": "Долгая доставка", "price": Decimal("4000.00"), "delivery_days": 7},
                ],
            }

        result = await recommend_price(
            fetch_offers, Decimal("5000.00"), Decimal("4500.00")
        )

        self.assertIsInstance(result["price"], Decimal)
        self.assertEqual(result["price"], Decimal("4728.00"))
        self.assertEqual(result["decision"], "APPLY")

    async def test_source_error_preserves_current_price_below_minimum(self):
        async def fetch_offers():
            raise OSError("Источник недоступен")

        result = await recommend_price(
            fetch_offers, Decimal("4000.00"), Decimal("4500.00")
        )

        self.assertEqual(result["price"], Decimal("4000.00"))
        self.assertEqual(result["decision"], "HOLD")