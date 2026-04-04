import asyncio
from contextlib import asynccontextmanager


class AsyncStampedeProtection:
	def __init__(self):
		self._global_lock = asyncio.Lock()
		self._locks = {}

	async def _get_lock(self, key):
		async with self._global_lock:
			if key not in self._locks:
				self._locks[key] = asyncio.Lock()
			return self._locks[key]

	@asynccontextmanager
	async def lock(self, key):
		lock = await self._get_lock(key)
		await lock.acquire()
		try:
			yield
		finally:
			lock.release()
