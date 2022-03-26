import ctypes
import time
import json

Titles = []
titles_short = []


def get_window_names():

    def foreach_window(hwnd):
        if ctypes.windll.user32.IsWindowVisible(hwnd):  # if window is visible
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)  # get window text size
            buff = ctypes.create_unicode_buffer(length + 1)  # get buffer size
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)  # get window text
            if len(buff.value) > 1:
                Titles.append(buff.value)
                res = buff.value.replace('\\', ' - ').split(' - ')
                res_buff = ''
                for _ in res:
                    res_buff = _
                titles_short.append([res_buff, buff.value])

    enum_windows = ctypes.windll.user32.EnumWindows
    enum_windows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int))(foreach_window), 0)
    print(titles_short)


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
        ctypes.windll.user32.MoveWindow(handle, x, y, width+50-(_*50), height, True)


if __name__ == '__main__':
    time.sleep(0)

    # load the settings json from the settings file into a buffer:
    settings = open("settings.wm", "r")
    json_buffer = settings.read()

    get_window_names()

    # convert json into a list of objects:
    if len(json_buffer) > 1:
        window_settings_array = json.loads(json_buffer)
        for setting in window_settings_array:
            if setting['is_minimized'] == 1:
                move_window(setting['name'], setting['x'], setting['y'], setting['width'], setting['height'], True)
            move_window(setting['name'], setting['x'], setting['y'], setting['width'], setting['height'], False)
