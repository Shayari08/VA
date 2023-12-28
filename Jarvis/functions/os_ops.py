import os
import subprocess as sp

paths = {
    'notepad': "C:\Windows\notepad.exe",
    'calculator': "C:\Windows\System32\calc.exe"
}

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notepad():
    try:
        sp.run(['notepad.exe'])
    except FileNotFoundError as e:
        print(f"Error: {e}")

def open_discord():
    os.startfile(paths['discord'])

def open_cmd():
    os.system('start cmd')

def open_calculator():
    sp.Popen(paths['calculator'])