import threading
import time
from typing import Any, Optional

from .base import BaseBackend


class MemoryBackend(BaseBackend):
	def __init__(self):
		self.store = {}
		self._lock = threading.RLock()

	def has(self, key: str) -> bool:
		with self._lock:
			return key in self.store

	def get(self, key: str) -> Optional[Any]:
		with self._lock:
			item = self.store.get(key)
			if not item:
				return None
			
			value, expires_at = item
			if expires_at and expires_at < time.time():
				self.store.pop(key, None)
				return None

			return value, expires_at

	def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
		with self._lock:
			expires_at = time.time() + ttl if ttl else None
			self.store[key] = (value, expires_at)

	def delete(self, key: str) -> None:
		with self._lock:
			self.store.pop(key, None)

	def clear(self) -> None:
		with self._lock:
			self.store.clear()
