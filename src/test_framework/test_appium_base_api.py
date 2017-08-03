import unittest
from com.framework.core.appiumdriver.AppiumBaseApi import AppiumDriver
from com.framework.core.initdriver.InitAppiumDriver import InitDriverOption
from appium.webdriver.common.mobileby import By


class TestAppiumBaseApi(unittest.TestCase):
    def setUp(self):
        self.drvier = InitDriverOption().get_android_driver()
        self.appiumapi = AppiumDriver(self.drvier)

    def tearDown(self):
        self.drvier.quit()

    # @unittest.skip("skip 'test_is_displayed' func")
    def test_is_displayed(self):
        print self.appiumapi.is_displayed(By.ID, "com.youku.phone:id/img_user")

    @unittest.skip("skip 'test_find_element_by_want' func")
    def test_find_element_by_want(self):
        print self.appiumapi.find_element_by_want(By.ID, "com.youku.phone:id/img_user", 5)

    def test_get_current_activity(self):
        print self.appiumapi.get_current_activity()


if __name__ == '__main__':
    unittest.main()
