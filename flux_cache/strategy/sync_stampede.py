from contextlib import contextmanager
import threading


class SyncStampedeProtection:
	def __init__(self):
		self._global_lock = threading.Lock()
		self._locks = {}

	def _get_lock(self, key):
		with self._global_lock:
			if key not in self._locks:
				self._locks[key] = threading.Lock()
			return self._locks[key]

	@contextmanager
	def lock(self, key):
		lock = self._get_lock(key)
		lock.acquire()
		try:
			yield
		finally:
			lock.release()
