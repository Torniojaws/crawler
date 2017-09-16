"""Config for the crawler"""

from os import makedirs
from os.path import abspath, dirname, exists, isfile, join
import configparser

from apps.rules.rules import Rules

# Some preliminary config, mostly for environment and logging setup
CURRENT_DIR = abspath(dirname(__file__))
PROJECT_ROOT = dirname(dirname(CURRENT_DIR))
configfile = configparser.ConfigParser()
configpath = abspath(join(CURRENT_DIR, "config.cfg"))
with open(configpath, "r") as cfg:
    configfile.read_file(cfg)


def create_logdir(path):
    """Check that our logdir and file exist. Create if not"""
    if isfile(path) is False:
        if exists(dirname(abspath(path))) is False:
            makedirs(dirname(abspath(path)))
            open(path, "w+")


class Config():
    """This configures the app behaviour for the site crawling."""
    SECRET_KEY = configfile.get("env", "secret")
    PROJECT_ROOT = PROJECT_ROOT
    RELATIVE_LOG_PATH = configfile.get("log", "path")
    LOGFILE = configfile.get("log", "file")

    log_full = join(PROJECT_ROOT, RELATIVE_LOG_PATH, LOGFILE)
    create_logdir(log_full)
    LOGPATH = log_full

    def __init__(self, period, requirements):
        """Setup the site-specific content requirements. The source can be anything, as long as the
        delimiter is specified in the first row of the file, following the string "delmiter",
        and the contents can be read."""
        if period:
            self.check_period = period
        else:
            # If no period was given, or it was "" or None, we default to 60 seconds
            self.check_period = 60
        req = Rules()
        # This is a list of dicts, where each dict has key=site, value=content requirement
        self.site_requirements = req.get(requirements)


class ProdConfig(Config):
    TIMEOUT_SECONDS = 5


class DevConfig(Config):
    TIMEOUT_SECONDS = 6


ENV = configfile.get("env", "env")


def get_config(ENV):
    if ENV == "prod":
        CONFIG = ProdConfig
    else:
        CONFIG = DevConfig
    return CONFIG


CONFIG = get_config(ENV)
