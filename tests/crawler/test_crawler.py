import os
import unittest

from datetime import datetime

from apps.config.config import CONFIG, create_logdir
from apps.crawler.crawler import Crawler


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()
        self.test_logpath = "test_crawlerlog"

    def test_getting_timediff(self):
        self.assertEquals(
            "1m 0s 0ms",
            self.crawler.get_timediff(
                datetime(2017, 9, 16, 3, 22, 10, 455000),
                datetime(2017, 9, 16, 3, 23, 10, 455000)
            )
        )
        self.assertEquals(
            "1m 1s 495ms",
            self.crawler.get_timediff(
                datetime(2017, 9, 16, 3, 22, 10, 455000),
                datetime(2017, 9, 16, 3, 23, 11, 950000)
            )
        )
        self.assertEquals(
            "0m 0s 100ms",
            self.crawler.get_timediff(
                datetime(2017, 9, 16, 3, 22, 10, 455000),
                datetime(2017, 9, 16, 3, 22, 10, 555000)
            )
        )

    def test_logfile(self):
        full = os.path.join(CONFIG.PROJECT_ROOT, self.test_logpath, "test.log")
        create_logdir(full)
        open(full, "w").close()

        page = "http://www.example.com"
        status = "OK"
        content = "OK"
        duration = "0m 1s 123ms"
        self.crawler.log_result(full, page, status, content, duration)

        with open(full, "r") as log:
            result = log.read()

        print("LOGFILE res: {}".format(result))
        self.assertTrue(
            (" - Crawler - Site: http://www.example.com, Status: OK, Content: OK, Time taken: "
                "0m 1s 123ms") in result[23:]  # We ignore the timestamp (first 23 characters)
        )

    def test_loading_page(self):
        full = os.path.join(CONFIG.PROJECT_ROOT, self.test_logpath, "test.log")
        create_logdir(full)
        open(full, "w").close()

        page = "http://juhau.mbnet.fi/sites.txt"
        content_requirement = "delimiter"
        self.crawler.load_page(full, page, content_requirement)

        with open(full, "r") as log:
            result = log.read().splitlines()[0]

        self.assertTrue(
            (" - Crawler - Site: http://juhau.mbnet.fi/sites.txt, Status: OK, Content: OK, "
                "Time taken: ") in result
        )

    def test_loading_page_that_results_in_error(self):
        full = os.path.join(CONFIG.PROJECT_ROOT, self.test_logpath, "test.log")
        create_logdir(full)
        open(full, "w").close()

        page = "http://www.doesnotexist.se"
        content_requirement = "delimiter"
        self.crawler.load_page(full, page, content_requirement)

        with open(full, "r") as log:
            result = log.read()

        self.assertTrue("ERROR" in result)

    def test_loading_page_that_timeouts(self):
        full = os.path.join(CONFIG.PROJECT_ROOT, self.test_logpath, "test.log")
        create_logdir(full)
        open(full, "w").close()

        # This is a bit hacky. There doesn't seem to be a better way to simulate Timeouts in
        # cross-platform Python. In pure Linux, you could run "nc -l 80" in subprocess
        page = "https://www.google.com:8999"
        content_requirement = "delimiter"
        self.crawler.load_page(full, page, content_requirement)

        with open(full, "r") as log:
            result = log.read()

        self.assertTrue("DOWN" in result)
