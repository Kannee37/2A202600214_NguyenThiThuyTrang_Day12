from datetime import datetime, timedelta


class SimpleRateLimiter:
    """
    In-memory rate limiter đơn giản cho demo/lab.
    Key: user_id
    Value: list các timestamp request trong 1 phút gần nhất
    """
    def __init__(self):
        self.storage: dict[str, list[datetime]] = {}

    def allow(self, user_id: str, limit_per_minute: int) -> bool:
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=1)

        requests = self.storage.get(user_id, [])
        requests = [ts for ts in requests if ts >= window_start]

        if len(requests) >= limit_per_minute:
            self.storage[user_id] = requests
            return False

        requests.append(now)
        self.storage[user_id] = requests
        return True


rate_limiter = SimpleRateLimiter()