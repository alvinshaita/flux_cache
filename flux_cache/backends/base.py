from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseBackend(ABC):

	@abstractmethod
	def has(self, key: str) -> bool:
		pass

	@abstractmethod
	def get(self, key: str) -> Optional[Any]:
		pass

	@abstractmethod
	def set(self, key: str, value: Optional[Any], ttl: Optional[int]) -> None:
		pass

	@abstractmethod
	def delete(self, key: str) -> None:
		pass

	@abstractmethod
	def clear(self) -> None:
		pass
