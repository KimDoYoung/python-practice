import win32gui
hwnd = win32gui.FindWindow(None, 'Untitled - Notepad')
print(hwnd)