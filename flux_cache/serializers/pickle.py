import pickle
from typing import Any, Optional

from .base import BaseSerializer


class PickleSerializer(BaseSerializer):

	def dumps(self, value: Optional[Any]) -> bytes:
		return pickle.dumps(value)

	def loads(self, data: bytes) -> Optional[Any]:
		return pickle.loads(data)
