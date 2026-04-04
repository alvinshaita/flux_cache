import unittest
from unittest.mock import MagicMock, patch

from flux_cache import cache


class TestCacheDecorator(unittest.TestCase):

    def setUp(self):
        self.backend_patcher = patch("flux_cache.core.MemoryBackend")
        self.key_patcher = patch("flux_cache.core.generate_cache_key")

        self.MockBackend = self.backend_patcher.start()
        self.mock_key = self.key_patcher.start()

        self.backend_instance = MagicMock()
        self.MockBackend.return_value = self.backend_instance

        self.mock_key.return_value = "test-key"

    def tearDown(self):
        self.backend_patcher.stop()
        self.key_patcher.stop()

    def test_cache_miss_calls_function_and_sets_cache(self):
        self.backend_instance.get.return_value = None

        @cache
        def add(x, y):
            return x + y

        result = add(2, 3)

        self.assertEqual(result, 5)
        self.backend_instance.set.assert_called_once_with(
            "test-key", 5, ttl=None)

    def test_cache_hit_returns_cached_value(self):
        self.backend_instance.get.return_value = 42, None

        @cache
        def add(x, y):
            return x + y

        result = add(2, 3)

        self.assertEqual(result, 42)
        self.backend_instance.get.assert_called_once_with("test-key")
        self.backend_instance.set.assert_not_called()

    # invalidation
    def test_invalidate_calls_backend_delete(self):
        @cache
        def add(x, y):
            return x + y

        add.invalidate(2, 3)

        self.backend_instance.delete.assert_called_once_with("test-key")

    # clear
    def test_clear_calls_backend_clear(self):
        @cache
        def add(x, y):
            return x + y

        add.clear()

        self.backend_instance.clear.assert_called_once()

    # key generation
    def test_generate_cache_key_called_correctly(self):
        self.backend_instance.get.return_value = None

        @cache
        def multiply(a, b):
            return a * b

        multiply(4, 5)

        self.mock_key.assert_called_once()
        args, kwargs = self.mock_key.call_args

        self.assertEqual(args[1], (4, 5))   # positional args
        self.assertEqual(kwargs, {})        # no kwargs

    # decorator with params
    def test_decorator_with_parameters(self):
        self.backend_instance.get.return_value = None

        @cache(backend=self.backend_instance)
        def subtract(x, y):
            return x - y

        result = subtract(5, 3)

        self.assertEqual(result, 2)
        self.backend_instance.set.assert_called_once()


if __name__ == "__main__":
    unittest.main()
