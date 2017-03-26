import unittest
from com.framework.core.appiumdriver.initdriver import InitDriverOption
from com.framework.core.appiumdriver.touchactions import AppTouchAction

class TouchAction(unittest.TestCase):
    def setUp(self):
        self.driver = InitDriverOption().get_android_driver()
        self.ac = AppTouchAction(self.driver)

    def test_AppTouchAction(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
