"""The main entry point for the app.

There are two arguments you can pass:
1. Time interval between site checks
2. The source of the site configuration data (URL or a file in the root of the project)

python app.py --period 60 --req site-requirements.txt
python app.py --period 45 --req http://www.example.com/site-requirements.txt

If the arg begins with "http", we assume an URI. Otherwise we attempt to load a file in the root
of the project.
"""

import argparse
import asyncio

from apps.config.config import Config, CONFIG
from apps.crawler.crawler import Crawler

parser = argparse.ArgumentParser()
parser.add_argument("--period", "-p", help="Time period between checks, in seconds")
parser.add_argument("--req", "-r", help="Source of site requirements. URL or filename")

args = parser.parse_args()
period = args.period
requirements = args.req

config = Config(period, requirements)
crawler = Crawler()


# This will run until the end of time, or at least until you close the app :)
# WARNING: If you close the app with Ctrl+C, it will not close until the *end* of the async wait!
# So if you have a long time period, the app will not stop for a long time.
async def crawl_loop(event_loop: asyncio.BaseEventLoop):
    try:
        while event_loop.is_running():
            for site_data in config.site_requirements:
                url = next(iter(site_data))
                content = site_data[url]
                print("Checking URL: {}".format(url))
                print("For content: {}".format(content))
                crawler.load_page(CONFIG.LOGPATH, url, content)
            print("Waiting {} seconds until checking the sites again.".format(period))
            await asyncio.sleep(float(period))
    except asyncio.CancelledError:
        print("Stopping")
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(crawl_loop(loop))
    future = asyncio.gather(task)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        future.cancel()
        loop.run_until_complete(future)
        loop.close()
