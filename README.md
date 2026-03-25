# Flux Cache

An extensible, and production-ready caching library for Python with built-in **stampede protection**, **async support**, and **pluggable backends**.

---


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
def get_data(x):
    print("Computing...")
    return x * 2

get_data(2)  # computes
get_data(2)  # cached
```

---

### Async Support

```python
import asyncio
from flux_cache import cache

@cache(ttl=60)
async def fetch_data(x):
    print("Fetching...")
    await asyncio.sleep(1)
    return x * 2

asyncio.run(fetch_data(2))
```

---

## Backends

### Memory Backend (Default)

```python
from flux_cache import cache
from flux_cache.backends import MemoryBackend

@cache(backend=MemoryBackend(), ttl=60)
def func():
    return "data"
```

---

### Redis Backend

```python
from flux_cache import cache
from flux_cache.backends import RedisBackend

backend = RedisBackend(host="localhost", port=6379)

@cache(backend=backend, ttl=60)
def func():
    return "data"
```

---

## Stampede Protection

Flux Cache prevents multiple concurrent calls from recomputing the same value.

### How it works:

* First request acquires a lock
* Other requests wait
* Cached value is reused after computation

Works for:

* Threads (sync)
* Async coroutines

---

## Cache Stats

Each cached function tracks performance:

```python
@cache()
def slow():
    return "done"

slow()
slow()

print(slow.stats.hits)   # 1
print(slow.stats.misses) # 1
```

---

## Cache Management

### Invalidate Specific Entry

```python
slow.invalidate()
slow.invalidate(1, 2, key="value")
```

### Clear Entire Cache

```python
slow.clear()
```

---

## Cache Key Generation

Flux Cache automatically generates keys using:

* Function name
* Module
* Arguments (args + kwargs)

This ensures:

* Deterministic caching
* No collisions

---

## Running Tests

```bash
pytest
```

---

## Extending Flux Cache

### Custom Backend

```python
from flux_cache.backends.base import BaseBackend

class CustomBackend(BaseBackend):
    def get(self, key):
        ...

    def set(self, key, value, ttl=None):
        ...

    def delete(self, key):
        ...

    def clear(self):
        ...
```

---

### Custom Serializer

```python
from flux_cache.serializers.base import BaseSerializer

class CustomSerializer(BaseSerializer):
    def dumps(self, value):
        ...

    def loads(self, value):
        ...
```


## License

MIT License

---

## Author

**Alvin Rombora**

---
