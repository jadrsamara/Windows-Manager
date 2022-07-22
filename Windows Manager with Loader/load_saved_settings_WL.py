# import json for reading and storing window settings:
import json
# import os to get the documents folder
import os
# import ctypes which allows calling functions in DLLs or shared libraries:
import ctypes
from ctypes import wintypes
# import time to load windows after set number of seconds
import time

titles_short = []
window_titles = []


def move_window(window_name, x, y, width, height, is_minimized):

    def get_window_handle(part_of_name: str):
        for name in titles_short:
            if part_of_name.__eq__(name[0]):
                return ctypes.windll.user32.FindWindowW(None, name[1])
        return 0

    handle = ctypes.windll.user32.FindWindowW(None, window_name)  # get handle for window_name

    if is_minimized:
        ctypes.windll.user32.ShowWindow(handle, 3)  # maximize no-scale = 3

    for _ in range(0, 2):
        if handle == 0:
            handle = get_window_handle(window_name)
        ctypes.windll.user32.ShowWindow(handle, 6)  # minimize = 6
        ctypes.windll.user32.ShowWindow(handle, 9)  # maximize = 9
        ctypes.windll.user32.MoveWindow(handle, x, y, width + 50 - (_ * 50), height, True)


def main():

    # load the settings json from the settings file into a buffer:
    settings = open(os.path.join(os.path.expanduser('~'), 'Documents\\WindowsManager', 'settings.wm'), 'r')

    json_buffer = settings.read()

    # convert json into a list of objects:
    if len(json_buffer) > 1:
        window_settings_array = json.loads(json_buffer)
        for setting in window_settings_array:
            if setting['is_minimized'] == 1:
                move_window(setting['name'], setting['x'], setting['y'], setting['width'], setting['height'], True)
            move_window(setting['name'], setting['x'], setting['y'], setting['width'], setting['height'], False)


if __name__ == '__main__':
    time.sleep(15)
    main()
