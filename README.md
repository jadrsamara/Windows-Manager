# Windows-Manager
Python program to save Windows's windows' positions :)

I personally use it to resize Discord and move it to a specific position on my second screen

![image](https://user-images.githubusercontent.com/77105910/180623848-56e26129-0b2e-4547-89df-f752dfabe93a.png)

## Dependencies

* Python 3.7
* python library: json
* python library: os
* python library: ctypes
* python library: wintypes from ctypes
* python library: threading
* python library: time
* python library: tkinter
* python library: win32com.client
* python library: winshell

## Testing

Tested on two 1080p screens with different scalings (100% and 125% scaling)

## Preview of the program V1:

Simple GUI that shows the saved settings on the left, and the current open windows on the right. Settings are saved in the Documents folder

![image](https://user-images.githubusercontent.com/77105910/180623312-fa2e5bce-0a1f-4cf1-8f90-92eaae9d504b.png) ![image](https://user-images.githubusercontent.com/77105910/180623969-a18045e3-1854-437e-8dcb-337194d9100b.png)


When a program is choosen, the window is highlighted 

![image](https://user-images.githubusercontent.com/77105910/180623331-3d7f4f3b-b3df-47b4-b140-06589ef6a6de.png)


If you choose to load settings at startup, a shortcut of the second python program is added to the startup folder. the program waits 15 seconds after startup (to give the programs a chance to load) then loads the saved windows saved settings. 

![image](https://user-images.githubusercontent.com/77105910/180623346-8affc085-1fd4-43a0-bc45-95386e2e8f1a.png)


