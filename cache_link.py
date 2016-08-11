import os
import sys

CACHE = "article.cache"

class CacheLink:

    def __init__(self):
        self.cache_file = CACHE
        self._init_file()
        self.records = {}
        self._load_cache()

    def _init_file(self):
        if not os.path.isfile(self.cache_file):
            with open(self.cache_file, "w") as f:
                pass

    def _load_cache(self):
        with open(self.cache_file, "r") as f:
            self.records = {record.strip() for record in f.readlines()}

    def link_in_cache(self, url):
        return url in self.records

    def cache_link(self, url):
        with open(self.cache_file, "a") as f:
            if not self.link_in_cache(url):
                f.write(url + "\n")
        self._load_cache()
            
if __name__ == "__main__":
    ca = CacheLink()
