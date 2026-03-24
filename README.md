# Flux Cache

An extensible caching library for Python with support for synchronous and asynchronous functions.

## Installation

```bash
pip install flux-cache[redis]
```

---

## Quick Start

### Basic Usage

```python
from flux_cache import cache

@cache(ttl=60)
def expensive_function(x, y):
    print("Computing...")
    return x + y

expensive_function(1, 2)  # computes
expensive_function(1, 2)  # cached
```

---

### Async Usage

```python
from flux_cache import async_cache

@async_cache(ttl=60)
async def fetch_data(x):
    return x * 2
```

---

## How It Works

* A cache key is generated using:

  * Function module
  * Function name
  * Arguments (args + kwargs)
* The key is hashed using SHA-256
* Values are stored in the backend along with optional expiration timestamps

---

## Cache Control

### Clear entire cache

```python
expensive_function.clear()
```

### Invalidate specific call

```python
expensive_function.invalidate(1, 2)
```

---

## Backends

### Default: In-Memory

Thread-safe, simple dictionary-based backend.

```python
from flux_cache.backends import MemoryBackend

@cache(backend=MemoryBackend())
def foo():
    return "bar"
```

### Custom Backend

Implement the `BaseBackend` interface:

```python
class BaseBackend:
    def get(self, key): ...
    def set(self, key, value, ttl=None): ...
    def delete(self, key): ...
    def clear(self): ...
```

---

## 🧪 Testing

Run tests using:

```bash
pytest
```

---

## 📄 License

MIT License
