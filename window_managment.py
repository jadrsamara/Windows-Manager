# import json for reading and storing window settings:
import json
# import ctypes which allows calling functions in DLLs or shared libraries:
import ctypes
from ctypes import wintypes

# window names:
titles = []
# windows to be saved:
saves = []


def get_window_names():
    """
    This function saves the visible windows names and positions in the list 'titles'
    """
    ctypes.windll.user32.SetProcessDPIAware()
    enum_windows = ctypes.windll.user32.EnumWindows
    enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

    def get_window_coordinates(hwnd):
        """ Returns a rect (x,y,w,h) for the specified window's area """

        user32 = ctypes.windll.user32

        # to get accurate width and height
        user32.SetProcessDPIAware()

        rect = ctypes.wintypes.RECT()

        if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            x1 = rect.left
            y1 = rect.top
            x2 = rect.right
            y2 = rect.bottom
            return int(str(x1)), int(str(y1)), int(str(x2)) - int(str(x1)), int(str(y2)) - int(str(y1))
        return None

    def foreach_window(hwnd, f):
        """
        This function gets the name of the windows and gets their position by calling the
        function:'get_window_coordinates', then saves the names and the coordinates (x, y, width, height)
        in the list:'titles' as a dictionary.
        :param hwnd: window handle
        :param f: next window handle (not used)
        :return: void
        """
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            if len(buff.value) > 1:
                x, y, width, height = get_window_coordinates(hwnd)
                if ' - ' in buff.value or '\\' in buff.value:
                    res = buff.value.replace('\\', ' - ').split(' - ')
                    res_buff = ''
                    for _ in res:
                        res_buff = _
                    titles.append({"name": res_buff, "x": x, "y": y, "width": width, "height": height, "is_minimized": 0})
                else:
                    titles.append({"name": buff.value, "x": x, "y": y, "width": width, "height": height, "is_minimized": 0})

    enum_windows(enum_windows_proc(foreach_window), 0)


def save_windows():
    """
    this function allows the user to choose which windows to save
    the windows are chosen from the list:'titles'
    the settings are saved into the file:'settings.wm' as a json
    :return: void
    """
    print('Windows:')
    for i in range(len(titles)):
        print(i+1, ': ', titles[i]['name'])

    print(' - - - - - - - - - - - - - - - - - - - -')
    choices = input('Please enter the numbers of the windows that you would like to save their position'
                    ' - separated by space:\n').split(' ')

    global saves
    saves = []
    for i in choices:
        saves.append(titles[int(i)-1])

    with open('settings.wm', 'w') as f:
        print(json.dumps(saves), file=f)


if __name__ == '__main__':
    # load the settings json from the settings file into a buffer:
    settings = open("settings.wm", "r")
    json_buffer = settings.read()

    # convert json into a list of objects:
    if len(json_buffer) > 1:
        window_settings_array = json.loads(json_buffer)
        print('settings:')
        counter = 1
        for setting in window_settings_array:
            print(counter, ': ', setting['name'])
            counter += 1
        print(' - - - - - - - - - - - - - - - - - - - -')
    else:
        print('no settings!')
        print(' - - - - - - - - - - - - - - - - - - - -')

    get_window_names()
    save_windows()

    input('\nDone! press any key to exit')
