import unittest
from com.framework.core.adb.commond import AdbCmder


class TestAdbCommand(unittest.TestCase):

    def setUp(self):
        self.cmd = AdbCmder()

    @unittest.skip("demonstrating skipping")
    def test_get_crash_log(self):
        self.cmd.get_crash_log()

    @unittest.skip("demonstrating skipping")
    def test_do_capture_window(self):
        self.cmd.do_capture_window()

    def test_get_ui_dump_xml(self):
        self.cmd.get_ui_dump_xml("W:\\OneDrive\\icloud\\AppiumTestProject\\testresult\\dumpxml")


if __name__ == '__main__':
    unittest.main()
