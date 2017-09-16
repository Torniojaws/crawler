"""This will crawl through a website with a configurable required string of text that
must exist in the page."""

from datetime import datetime
import logging
import math
import requests

from apps.config.config import CONFIG


class Crawler():
    def load_page(self, logpath, page, content_requirement):
        """Load a page and verify it meets the content requirement"""
        begin = datetime.now()

        content = "NO MATCH"
        try:
            # The request timeout is not the same thing as the time period of checks.
            response = requests.get(page, timeout=CONFIG.TIMEOUT_SECONDS)
            status = "OK"
            # Case-insensitive matching to the data we received.
            if content_requirement.lower() in response.text.lower():
                content = "OK"
        except requests.exceptions.Timeout:
            status = "DOWN"
        except:
            # Some other error
            status = "ERROR"

        end = datetime.now()
        timediff = self.get_timediff(begin, end)

        self.log_result(logpath, page, status, content, timediff)

    def log_result(self, logfile, page, status, content_valid, duration):
        """Log the result of the current crawl"""
        print("Site: {}, Status: {}, Content: {}, Time taken: {}".format(
            page,
            status,
            content_valid,
            duration
        ))

        # The log file must contain the checked URLs, their status and the response times.
        logging.basicConfig(
            filename=logfile,
            format="%(asctime)s - Crawler - %(message)s",
            level=logging.INFO
        )

        logging.info("Site: {}, Status: {}, Content: {}, Time taken: {}".format(
            page,
            status,
            content_valid,
            duration
        ))

    def get_timediff(self, start, end):
        """Return the time difference in a nice to read format"""
        time_delta = end - start
        days, hours, minutes, seconds = self.days_hours_minutes(time_delta)
        millis = math.ceil(time_delta.microseconds / 1000)

        return "{}m {}s {}ms".format(minutes, seconds, millis)

    def days_hours_minutes(self, td):
        return td.days, td.seconds//3600, (td.seconds//60) % 60, (td.seconds % 60)
