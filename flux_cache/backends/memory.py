import threading
import time
from typing import Any, Optional

from .base import BaseBackend
from ..serializers import PickleSerializer


class MemoryBackend(BaseBackend):
	def __init__(self, serializer=None):
		self.store = {}
		self.serializer = serializer or PickleSerializer()
		self._lock = threading.RLock()

	def has(self, key: str) -> bool:
		with self._lock:
			return key in self.store

	def get(self, key: str) -> Optional[Any]:
		with self._lock:
			cached = self.store.get(key)
			if cached is None:
				return None

			value, expires_at = cached
			if expires_at and expires_at < time.time():
				self.store.pop(key, None)
				return None

			deserialized_value = self.serializer.loads(value)

			return deserialized_value, expires_at

	def set(
		self, key: str, value: Optional[Any], ttl: Optional[int] = None
	) -> None:
		with self._lock:
			serilized_value = self.serializer.dumps(value)
			expires_at = time.time() + ttl if ttl else None

			self.store[key] = (serilized_value, expires_at)

	def delete(self, key: str) -> None:
		with self._lock:
			self.store.pop(key, None)

	def clear(self) -> None:
		with self._lock:
			self.store.clear()
