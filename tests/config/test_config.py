import os
import shutil
import unittest

from apps.config.config import Config, create_logdir, CONFIG, get_config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.filename = "site-requirements.txt"
        self.test_logpath = "test_configlog"

    def tearDown(self):
        if os.path.exists(self.test_logpath):
            shutil.rmtree(self.test_logpath)

    def test_config_without_time_period(self):
        config = Config(None, self.filename)

        self.assertEquals(60, config.check_period)

    def test_config_with_valid_time_period(self):
        config = Config(27, self.filename)

        self.assertEquals(27, config.check_period)

    def test_create_logdir(self):
        full = os.path.join(CONFIG.PROJECT_ROOT, self.test_logpath, "testfile.log")
        create_logdir(full)

        self.assertTrue(os.path.exists(full))

    def test_getting_prod_env_config(self):
        config = get_config("prod")

        self.assertEquals(5, config.TIMEOUT_SECONDS)
