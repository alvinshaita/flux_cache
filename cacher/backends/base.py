from abc import ABC, abstractmethod


class BaseBackend(ABC):

	@abstractmethod
	def has(self, key):
		pass

	@abstractmethod
	def get(self, key):
		pass

	@abstractmethod
	def set(self, key, value):
		pass

	@abstractmethod
	def delete(self, key):
		pass

	@abstractmethod
	def clear(self):
		pass
