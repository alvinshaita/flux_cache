import json
from typing import Any, Optional

from .base import BaseSerializer


class JsonSerializer(BaseSerializer):

	def dumps(self, value: Optional[Any]) -> bytes:
		return json.dumps(value)

	def loads(self, data: bytes) -> Optional[Any]:
		return json.loads(data)
