# import json for reading and storing window settings:
import json
# import ctypes which allows calling functions in DLLs or shared libraries:
import ctypes
import threading
from ctypes import wintypes
from tkinter import *

titles_short = []
window_titles = []
choices = []


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
                    window_titles.append(
                        {"name": res_buff, "x": x, "y": y, "width": width, "height": height, "is_minimized": 0})
                    titles_short.append([res_buff, buff.value])
                else:
                    window_titles.append(
                        {"name": buff.value, "x": x, "y": y, "width": width, "height": height, "is_minimized": 0})

    global titles_short, window_titles
    window_titles = []
    titles_short = []
    enum_windows(enum_windows_proc(foreach_window), 0)


def save_windows():
    """
    this function allows the user to choose which windows to save
    the windows are chosen from the list:'titles'
    the settings are saved into the file:'settings.wm' as a json
    :return: void
    """

    def click():
        global choices
        choices = []
        for selection in list_of_windows.curselection():
            choices.append(list_of_windows.get(selection).split(':  ')[0])
        save()
        if len(list_of_windows.curselection()) < 1:
            label_2['text'] = 'error'
            return 0

    def save():
        saves = []
        for i in choices:
            saves.append(window_titles[int(i) - 1])

        with open('settings.wm', 'w') as f:
            print(json.dumps(saves), file=f)

        label_2['text'] = 'Saved!'
        reload_settings()

    def terminate():
        window.destroy()

    def start_at_startup():
        label_2['text'] = 'Soon.'

    def run():
        # load the settings json from the settings file into a buffer:
        settings = open("settings.wm", "r")
        json_buffer = settings.read()

        # convert json into a list of objects:
        if len(json_buffer) > 1:
            window_settings_array = json.loads(json_buffer)
            for setting in window_settings_array:
                if setting['is_minimized'] == 1:
                    move_window(setting['name'], setting['x'], setting['y'], setting['width'], setting['height'], True)
                move_window(setting['name'], setting['x'], setting['y'], setting['width'], setting['height'], False)

        label_2['text'] = 'Loaded!'

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

    def reload_settings():
        # load the settings json from the settings file into a buffer:
        settings = open("settings.wm", "r")
        json_buffer = settings.read()
        if len(json_buffer) > 1:
            window_settings_array = json.loads(json_buffer)
        else:
            window_settings_array = [
                {"name": "No settings", "x": 0, "y": 0, "width": 0, "height": 0, "is_minimized": 0}]

        # for scrolling vertically
        y_2_scrollbar = Scrollbar(window)
        y_2_scrollbar.grid(row=2, column=2, sticky=E)
        label = Label(window,
                      text="Current settings :  ",
                      font=("Times New Roman", 10),
                      padx=10, pady=0)
        label.grid(row=1, column=1, sticky=E)

        list_of_settings = Listbox(window, selectmode="multiple", yscrollcommand=y_2_scrollbar.set)
        # Widget expands horizontally and
        # vertically by assigning both to
        # fill option
        list_of_settings.grid(row=2, column=1, sticky=E)
        list_of_settings.delete(0, END)
        for each_item_ in range(len(window_settings_array)):
            list_of_settings.insert(END, ' ' + str(each_item_ + 1) + ' :  ' + window_settings_array[each_item_]['name'])
            list_of_settings.itemconfig(each_item_, bg="white")

        # Attach listbox to vertical scrollbar
        y_2_scrollbar.config(command=list_of_settings.yview)

    def reload_windows():
        get_window_names()
        list_of_windows.delete(0, END)
        for each_item_ in range(len(window_titles)):
            list_of_windows.insert(END, ' ' + str(each_item_ + 1) + ' :  ' + window_titles[each_item_]['name'])
            list_of_windows.itemconfig(each_item_, bg="white")

    window = Tk()
    window.title('Windows Manager')

    reload_settings()

    # for scrolling vertically
    y_scrollbar = Scrollbar(window)
    y_scrollbar.grid(row=2, column=4, sticky=E)
    label = Label(window,
                  text="Select the programs :  ",
                  font=("Times New Roman", 10),
                  padx=10, pady=10)
    label.grid(row=1, column=5, sticky=W)

    list_of_windows = Listbox(window, selectmode="multiple", yscrollcommand=y_scrollbar.set)
    # Widget expands horizontally and
    # vertically by assigning both to
    # fill option
    list_of_windows.grid(row=2, column=5, sticky=W)
    for each_item in range(len(window_titles)):
        list_of_windows.insert(END, ' ' + str(each_item + 1) + ' :  ' + window_titles[each_item]['name'])
        list_of_windows.itemconfig(each_item, bg="white")

    # Attach listbox to vertical scrollbar
    y_scrollbar.config(command=list_of_windows.yview)

    reload_s_button = Button(window, text="Reload Settings", command=reload_settings)
    reload_s_button.grid(row=3, column=1, sticky=E)

    reload_w_button = Button(window, text="Reload Windows", command=reload_windows)
    reload_w_button.grid(row=3, column=5, sticky=W)

    save_button = Button(window, text="Load", command=run)
    save_button.grid(row=4, column=1, sticky=E)

    save_button = Button(window, text="Save", command=click)
    save_button.grid(row=4, column=5, sticky=W)

    label_2 = Label(window, text="", font=("Times New Roman", 10), padx=10, pady=10)
    label_2.grid(row=6, column=5, sticky=E)

    quit_button = Button(window, text="run at startup", command=start_at_startup)
    quit_button.grid(row=5, column=3, sticky=S)

    quit_button = Button(window, text="quit", command=terminate)
    quit_button.grid(row=6, column=3, sticky=N)

    window.mainloop()


if __name__ == '__main__':
    get_window_names()
    gui_thread = threading.Thread(target=save_windows())
    gui_thread.start()
