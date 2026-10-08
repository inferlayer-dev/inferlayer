import time
import hashlib


class Cache:
    def __init__(self, ttl=3600):
        self.ttl = ttl
        self.store = {}

    def _key(self, prompt):
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt):
        k = self._key(prompt)
        if k in self.store:
            value, ts = self.store[k]
            if time.time() - ts < self.ttl:
                return value
            del self.store[k]
        return None

    def set(self, prompt, value):
        self.store[self._key(prompt)] = (value, time.time())


class Router:
    def __init__(self, providers):
        self.providers = providers

    def route(self, prompt):
        for provider in self.providers:
            try:
                return self._call(provider, prompt)
            except Exception:
                continue
        raise RuntimeError("all providers failed")

    def _call(self, provider, prompt):
        # replace with real provider sdk calls
        return f"[{provider}] response to: {prompt}"


class InferLayer:
    def __init__(self, providers, ttl=3600):
        self.router = Router(providers)
        self.cache = Cache(ttl=ttl)

    def ask(self, prompt):
        cached = self.cache.get(prompt)
        if cached is not None:
            return cached
        result = self.router.route(prompt)
        self.cache.set(prompt, result)
        return result
