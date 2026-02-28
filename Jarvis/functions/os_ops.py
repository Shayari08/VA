import os
import glob
import subprocess as sp


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_notepad():
    try:
        sp.run(['notepad.exe'])
    except FileNotFoundError as e:
        print(f"Error opening Notepad: {e}")


def open_discord():
    # Try the standard install location (version-agnostic glob)
    pattern = os.path.join(
        os.environ.get('LOCALAPPDATA', ''), 'Discord', 'app-*', 'Discord.exe'
    )
    matches = glob.glob(pattern)
    if matches:
        sp.Popen(matches[-1])  # Use the most recent version found
    else:
        # Fall back to the URI scheme if the executable is not found
        sp.run('start discord://', shell=True)


def open_cmd():
    os.system('start cmd')


def open_calculator():
    sp.Popen(r'C:\Windows\System32\calc.exe')
