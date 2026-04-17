from datetime import datetime
from app.config import settings


class SimpleBudgetTracker:
    def __init__(self):
        self.storage = {}

    def _key(self, user_id: str):
        month = datetime.utcnow().strftime("%Y-%m")
        return f"{user_id}:{month}"

    def get_spent(self, user_id: str):
        return self.storage.get(self._key(user_id), 0.0)

    def check_budget(self, user_id: str, estimated_cost: float):
        current = self.get_spent(user_id)
        return (current + estimated_cost) <= settings.MONTHLY_BUDGET_USD

    def add_cost(self, user_id: str, cost: float):
        key = self._key(user_id)
        current = self.storage.get(key, 0.0)
        self.storage[key] = current + cost


budget_tracker = SimpleBudgetTracker()