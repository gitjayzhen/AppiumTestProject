import unittest
from com.framework.core.appiumdriver.appiumbaseapi import AppiumDriver
from com.framework.core.initdriver.initappiumdriver import InitDriverOption
import subprocess


class TestAppiumBaseApi(unittest.TestCase):
    def setUp(self):
        self.drvier = InitDriverOption().get_android_driver()
        self.appiumapi = AppiumDriver(self.drvier)

    def tearDown(self):
        self.drvier.quit()

    def test_by_id(self):
        self.appiumapi.find_element_By_Id("test")


if __name__ == '__main__':
    unittest.main()
