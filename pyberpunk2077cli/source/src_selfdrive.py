from pyberpunk2077cli.utils import image_processing
from pynput.mouse import Button, Controller
from pyberpunk2077cli.env import *
import time


class Delamain:
    def __init__(self):
        self.screen_size = None
        self.gap_drive_time = GAP_DRIVE_TIME
        self.mouse = Controller()
        self.mouse.position = (10, 20)

    def start(self, mode):
        lane_1, lane_2 = image_processing.get_lanes(lines=mode)
        return lane_1, lane_2

    def front(self):
        self.mouse.press(Button.middle)
        self.mouse.release(Button.left)
        self.mouse.release(Button.right)
        time.sleep(self.gap_drive_time)
        self.mouse.release(Button.middle)

    def left(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.right)
        time.sleep(self.gap_drive_time)
        self.mouse.release(Button.left)

    def right(self):
        self.mouse.press(Button.right)
        self.mouse.release(Button.left)
        time.sleep(self.gap_drive_time)
        self.mouse.release(Button.right)

    def check_stop(self):
        return image_processing.stop_key()
