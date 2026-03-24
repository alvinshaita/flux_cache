class CacheStats:
	def __init__(self):
		self.hits = 0
		self.misses = 0

	def hit(self):
		self.hits += 1

	def miss(self):
		self.misses += 1

	@property
	def ratio(self):
		total = self.hits + self.misses
		return self.hits / total if total else 0
