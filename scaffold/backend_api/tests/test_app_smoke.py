from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app


class TestAppSmoke(unittest.TestCase):
    def test_health_endpoint_imports_and_responds(self) -> None:
        with TestClient(app) as client:
            response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["service"], "sajuwonhae-api")


if __name__ == "__main__":
    unittest.main()