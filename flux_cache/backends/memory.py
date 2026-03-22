import threading
from typing import Any, Optional

from flux_cache.backends.base import BaseBackend


class MemoryBackend(BaseBackend):
	def __init__(self):
		self.store = {}
		self._lock = threading.RLock()

	def has(self, key: str) -> bool:
		with self._lock:
			return key in self.store

	def get(self, key: str) -> Optional[Any]:
		with self._lock:
			return self.store.get(key)

	def set(self, key: str, value: Any) -> None:
		with self._lock:
			self.store[key] = value

	def delete(self, key: str) -> None:
		with self._lock:
			self.store.pop(key, None)

	def clear(self) -> None:
		with self._lock:
			self.store.clear()
