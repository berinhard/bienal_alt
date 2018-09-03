from django.core.cache import cache
from decorator import decorator


class ActionCache():

    def __init__(self, action_slug, language):
        self.action_slug = action_slug
        self.language = language

    @property
    def key_prefix(self):
        return '{}-{}-'.format(self.language, self.action_slug)

    def _get_key(self, key):
        return self.key_prefix + key

    def get(self, cache_key, default=None):
        key = self._get_key(cache_key)
        value = cache.get(key)
        if value is None:
            return default
        return value

    def set(self, cache_key, value, *args, **kwargs):
        key = self._get_key(cache_key)
        cache.set(key, value, *args, **kwargs)

    def delete(self, cache_key):
        key = self._get_key(cache_key)
        cache.delete(key)

    def clear(self):
        search = self.key_prefix + '*'
        for key in cache.iter_keys(search):
            cache.delete(key)

        for key in cache.keys('*.home.*'):
            cache.delete(key)
