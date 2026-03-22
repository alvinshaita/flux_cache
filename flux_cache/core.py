import functools
from typing import Callable, Optional

from flux_cache.backends import MemoryBackend
from flux_cache.utils import generate_cache_key

def cache(
	func: Optional[Callable] = None,
	*,
	backend = None
):
	if backend is None:
		backend = MemoryBackend()

	if func is None:
		return lambda f: cache(f, backend=backend)

	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		key = generate_cache_key(func, args, kwargs)

		if backend.has(key):
			return backend.get(key)

		result = func(*args, **kwargs)
		backend.set(key, result)

		return result

	def clear():
		backend.clear()

	def invalidate(*args, **kwargs):
		key = generate_cache_key(func, args, kwargs)
		backend.delete(key)

	wrapper.clear = clear
	wrapper.invalidate = invalidate

	return wrapper
