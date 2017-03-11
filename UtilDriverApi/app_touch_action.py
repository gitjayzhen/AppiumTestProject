#!/usr/bin/env python

class AppTouchAction():
    def __init__(self, driver=None):
        self._driver = driver
        self._actions = []

    def tap(self, element=None, x=None, y=None, count=1):
        """Perform a tap action on the element
        :Args:
         - element - the element to tap
         - x - (optional) x coordinate to tap, relative to the top left corner of the element.
         - y - (optional) y coordinate. If y is used, x must also be set, and vice versa
        :Usage:
        """
        return self

    def press(self, el=None, x=None, y=None):
        """Begin a chain with a press down action at a particular element or point
        """
        return self

    def long_press(self, el=None, x=None, y=None, duration=1000):
        """Begin a chain with a press down that lasts `duration` milliseconds
        """
        return self

    def wait(self, ms=0):
        """Pause for `ms` milliseconds.
        """
        return self

    def move_to(self, el=None, x=None, y=None):
        """Move the pointer from the previous point to the element or point specified
        """
        return self

    def release(self):
        """End the action by lifting the pointer off the screen
        """
        return self

    def perform(self):
        """Perform the action by sending the commands to the server to be operated upon
        """
        # get rid of actions so the object can be reused
        return self

    def pinch(self):
        '''
        Places two fingers at the edges of the screen and brings them together. 在 0% 到 100% 内双指缩放屏幕，
        '''
        driver.pinch(element=el)
    def zoom(self):
        '''
        放大屏幕 在 100% 以上放大屏幕
        '''
        driver.zoom(element=el)
    def shake(self):
        '''
        模拟设备摇晃
        '''
        driver.shake()

 # convenience method added to Appium (NOT Selenium 3)
    def scroll(self, origin_el, destination_el):
        """Scrolls from one element to another
        :Args:
         - originalEl - the element from which to being scrolling
         - destinationEl - the element to scroll to
        :Usage:
            driver.scroll(el1, el2)
        """
        return self

    # convenience method added to Appium (NOT Selenium 3)
    def drag_and_drop(self, origin_el, destination_el):
        """Drag the origin element to the destination element
        :Args:
         - originEl - the element to drag
         - destinationEl - the element to drag to
        """
        return self

    # convenience method added to Appium (NOT Selenium 3)
    def flick(self, start_x, start_y, end_x, end_y):
        """Flick from one point to another point.
        :Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - end_x - x-coordinate at which to stop
         - end_y - y-coordinate at which to stop
        :Usage:
            driver.flick(100, 100, 100, 400)
        """
        return self


