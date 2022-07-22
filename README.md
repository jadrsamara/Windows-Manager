# Windows-Manager
Python program to save Windows's windows' positions :)

## Preview of the program V0.1:

https://user-images.githubusercontent.com/77105910/160248828-77fd11d2-00ca-4a6f-9953-32db125d6093.mp4

### Run at startup
to run the program at the start up make a shortcut of the `windows_manager_startup.py`, and move the shortcut into the `startup` folder.
the startup folder can be found here:
```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```
and set the timer from the code as in here:
```python
if __name__ == '__main__':
  time.sleep(0)
  ...
```
soon I will make a small python program to set a timer, or to run after all the programs start.
