import functools
import inspect
from typing import Callable, Optional

from .backends import MemoryBackend
from .utils import generate_cache_key

def cache(
	func: Optional[Callable] = None,
	*,
	ttl: Optional[int] = None,
	backend = None
):
	if backend is None:
		backend = MemoryBackend()

	if func is None:
		return lambda f: cache(f, ttl=ttl, backend=backend)

	is_async = inspect.iscoroutinefunction(func)

	# asynchronous wrapper
	@functools.wraps(func)
	async def async_wrapper(*args, **kwargs):
		key = generate_cache_key(func, args, kwargs)

		item = backend.get(key)
		if item is not None:
			value, _ = item
			return value

		result = await func(*args, **kwargs)
		backend.set(key, result, ttl=ttl)
		return result

	# synchronous wrapper
	@functools.wraps(func)
	def sync_wrapper(*args, **kwargs):
		key = generate_cache_key(func, args, kwargs)

		item = backend.get(key)
		if item is not None:
			value, _ = item
			return value

		result = func(*args, **kwargs)
		backend.set(key, result, ttl=ttl)
		return result

	wrapper = async_wrapper if is_async else sync_wrapper

	def invalidate(*args, **kwargs):
		key = generate_cache_key(func, args, kwargs)
		backend.delete(key)

	wrapper.clear = backend.clear
	wrapper.invalidate = invalidate

	return wrapper
