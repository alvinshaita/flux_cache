from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseSerializer(ABC):

	@abstractmethod
	def dumps(self, value: Optional[Any]) -> bytes:
		pass

	@abstractmethod
	def loads(self, data: bytes) -> Optional[Any]:
		pass
