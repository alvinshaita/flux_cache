import functools

from cacher.backends.memory import MemoryBackend
from cacher.utils import generate_cache_key

def cache(func=None, *, a=None, b=None):
	backend = MemoryBackend()

	if func is None:
		def wrapper_decorator(f):
			return cache(f, a=a, b=b)
		return wrapper_decorator

	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		key = generate_cache_key(func, args, kwargs)

		if backend.has(key):
			return backend.get(key)

		result = func(*args, **kwargs)
		backend.set(key, result)

		return result

	return wrapper
