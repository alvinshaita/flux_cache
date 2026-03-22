from flux_cache.backends.base import BaseBackend


class MemoryBackend(BaseBackend):
	def __init__(self):
		self.store = {}

	def has(self, key):
		return key in self.store

	def get(self, key):
		return self.store.get(key)

	def set(self, key, value):
		self.store[key] = value

	def delete(self, key):
		self.store.pop(key, None)

	def clear(self):
		self.store.clear()
