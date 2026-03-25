import hashlib
import os
from pathlib import Path
import time
from typing import Any, Optional

from .base import BaseBackend
from ..serializers import PickleSerializer


class FileBackend(BaseBackend):
	def __init__(self,
		directory="/tmp/flux_cache",
		serializer=None
	):
		self.directory = directory
		self.serializer = serializer or PickleSerializer()

		os.makedirs(directory, exist_ok=True)

	def _path(self, key):
		hashed = hashlib.sha256(key.encode()).hexdigest()
		return os.path.join(self.directory, hashed)

	def has(self, key: str) -> bool:
		path = self._path(key)
		return os.path.exists(path)

	def get(self, key: str) -> Optional[Any]:
		path = self._path(key)

		if not os.path.exists(path):
			return None

		with open(path, "rb") as f:
			value, expires_at = self.serializer.loads(f.read())
			f.flush()
			os.fsync(f.fileno())

		if expires_at and expires_at < time.time():
			try:
				os.remove(path)
			except:
				pass

			return None

		return value, expires_at

	def set(self, key: str, value: Optional[Any], ttl: Optional[int]) -> None:
		path = self._path(key)
		expires_at = time.time() + ttl if ttl else None

		serialized_value = self.serializer.dumps((value, expires_at))

		with open(path, "wb") as f:
			f.write(serialized_value)
			f.flush()
			os.fsync(f.fileno())

	def delete(self, key: str) -> None:
		path = self._path(key)
		try:
			os.remove(path)
		except:
			pass

	def clear(self) -> None:
		for file in os.listdir(self.directory):
			file_path = os.path.join(self.directory, file)
			try:
				os.remove(file_path)
			except:
				pass
