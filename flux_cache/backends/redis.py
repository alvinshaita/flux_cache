import json
import threading
import time
from typing import Any, Optional

from .base import BaseBackend
from ..serializers import PickleSerializer


class RedisBackend(BaseBackend):
	def __init__(self,
		url="redis://localhost:6379/0",
		serializer=None,
	):
		try:
			import redis
		except ImportError:
			raise ImportError(
				"RedisBackend requires 'redis' package.\n"
				"Install with: pip install flux-cache[redis]"
			)
		self.prefix = "flux-cache"
		self.red = redis.Redis.from_url(url)
		self.serializer = serializer or PickleSerializer()

	def _key(self, key: str) -> str:
		return f"{self.prefix}:{key}"

	def has(self, key: str) -> bool:
		namespaced_key = self._key(key)
		present = self.red.exists(namespaced_key)
		return True if present == 1 else False

	def get(self, key: str) -> Optional[Any]:
		namespaced_key = self._key(key)
		value = self.red.get(namespaced_key)
		if value is None:
			return None

		deserialized_value = self.serializer.loads(value)
		return deserialized_value, None

	def set(self, key: str, value: Optional[Any], ttl: Optional[int] = None) -> None:
		serialized_value = self.serializer.dumps(value)
		namespaced_key = self._key(key)
		self.red.set(namespaced_key, serialized_value, ex=ttl)

	def delete(self, key: str) -> None:
		namespaced_key = self._key(key)
		self.red.delete(namespaced_key)

	def clear(self) -> None:
		keys = self.red.keys(f"{self.prefix}*")
		if keys:
			self.red.delete(*keys)
