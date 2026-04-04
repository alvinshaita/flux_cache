import hashlib
import inspect
import pickle


def generate_cache_key(func, args, kwargs) -> str:
	sig = inspect.signature(func)
	bound = sig.bind(*args, **kwargs)
	bound.apply_defaults()

	normalized_args = tuple(
		(k, bound.arguments[k])
		for k in sig.parameters
	)

	key_data = (
		func.__module__,
		func.__name__,
		normalized_args
	)

	raw_data = pickle.dumps(key_data)
	return hashlib.sha256(raw_data).hexdigest()
