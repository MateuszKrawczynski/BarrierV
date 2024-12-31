import os
if open("install.txt","r").read() == "false":
    os.system("pip install -r requirements.txt")
    open("install.txt" , "w").write("true")
os.system("python main.pyw")