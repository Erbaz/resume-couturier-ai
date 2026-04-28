import datetime
import pytz
from cachetools import TTLCache

class RequestCacheManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestCacheManager, cls).__new__(cls)
            # maxsize to 10000 users, ttl to 24 hours (86400 seconds)
            cls._instance.cache = TTLCache(maxsize=10000, ttl=86400)
            cls._instance.current_day = cls._instance._get_current_pt_day()
        return cls._instance

    def _get_current_pt_day(self):
        # GCP quota resets at midnight Pacific Time
        pt_tz = pytz.timezone("America/Los_Angeles")
        return datetime.datetime.now(pt_tz).date()

    def _check_and_reset_cache(self):
        current_day = self._get_current_pt_day()
        if current_day != self.current_day:
            self.cache.clear()
            self.current_day = current_day

    def increment_user_request(self, email: str):
        self._check_and_reset_cache()
        if email in self.cache:
            self.cache[email] += 1
        else:
            self.cache[email] = 1
        return self.cache[email]
    
    def get_user_request_count(self, email: str):
        self._check_and_reset_cache()
        return self.cache.get(email, 0)

request_cache = RequestCacheManager()
