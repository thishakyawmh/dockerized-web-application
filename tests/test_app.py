import unittest
from unittest.mock import patch

import app as application


class FakeRedis:
    def __init__(self, visit_count=1, should_fail=False):
        self.visit_count = visit_count
        self.should_fail = should_fail

    def incr(self, _key):
        if self.should_fail:
            raise application.redis.RedisError("Redis unavailable")
        self.visit_count += 1
        return self.visit_count

    def ping(self):
        if self.should_fail:
            raise application.redis.RedisError("Redis unavailable")
        return True


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.client = application.app.test_client()

    def test_home_increments_visit_counter(self):
        fake_redis = FakeRedis(visit_count=4)
        with patch.object(application, "client", fake_redis):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Redis has counted <strong>5</strong> page visits.", response.get_data(as_text=True))

    def test_health_returns_healthy_when_redis_is_available(self):
        with patch.object(application, "client", FakeRedis()):
            response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "healthy", "redis": "connected"})

    def test_health_returns_503_when_redis_is_unavailable(self):
        with patch.object(application, "client", FakeRedis(should_fail=True)):
            response = self.client.get("/health")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json(), {"status": "unhealthy", "redis": "unavailable"})


if __name__ == "__main__":
    unittest.main()
