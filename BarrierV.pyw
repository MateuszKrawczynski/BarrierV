import os
import sys
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-run the script as admin
    print("Requesting administrator privileges...")
    script = sys.executable
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
    except Exception as e:
        print(f"Failed to elevate: {e}")
    sys.exit(0)
else:
    if open("install.txt","r").read() == "false":
        os.system("pip install -r requirements.txt")
        open("install.txt" , "w").write("true")
    os.system("start /b pythonw main.pyw")