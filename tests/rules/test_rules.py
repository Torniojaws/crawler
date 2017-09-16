import unittest

from apps.rules.rules import Rules


class TestRules(unittest.TestCase):
    def setUp(self):
        self.rules = Rules()

    def test_getting_remote_list(self):
        # XXX: This is a brittle test, but will do for demo purposes
        uri = "http://juhau.mbnet.fi/sites.txt"
        result = self.rules.get(uri)

        self.assertEquals(3, len(result))
        self.assertEquals("http://www.example.com", next(iter(result[0])))
        self.assertEquals("Weather forecast for", list(result[2].values())[0])

    def test_getting_local_list(self):
        filename = "site-requirements.txt"
        result = self.rules.get(filename)

        self.assertEquals(4, len(result))
        self.assertEquals("http://www.example.com", next(iter(result[0])))
        self.assertEquals("News Limited Copyright", list(result[2].values())[0])
