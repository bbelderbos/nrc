import sys
import unittest
from nrc import *

CACHE = "article.cache"

class TestNrc(unittest.TestCase):

    def setUp(self):
        with open("testfiles/index.html", "rt") as f:
            html = f.read()
        self.articles = get_articles(html)
        self._clean_cache()
    
    def _clean_cache(self):
        with open(CACHE, "w") as f:
            pass

    def test_output(self):
        output = generate_html_output(self.articles, cache_enabled=False)
        self.assertEqual(len(output), 42)

    def test_cache(self):
        output = generate_html_output(self.articles, cache_enabled=False)
        self.assertEqual(len(output), 42)
        output = generate_html_output(self.articles, cache_enabled=True)
        self.assertEqual(len(output), 0)
        self._delete_two_links()
        output = generate_html_output(self.articles, cache_enabled=True)
        self.assertEqual(len(output), 2)
        output = generate_html_output(self.articles, cache_enabled=True)
        self.assertEqual(len(output), 0)

    def _delete_two_links(self):
        urls = cache_link.records
        with open(CACHE, "w") as f:
            for url in list(urls)[0:-2]:
                f.write(url + "\n")
        cache_link._load_cache()

if __name__ == "__main__":
    unittest.main()
