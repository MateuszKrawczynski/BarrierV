import eel
import requests
import base64
import time
from tkinter import filedialog
import tkinter
import webbrowser
import os , shutil , subprocess

API_KEY = open("apikey.txt","r").read()

rtp = "BarrierV-rtp.exe" # change to .exe after compiling
if rtp not in os.listdir(f'C:\\Users\\{os.getenv("username")}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'):
    try:
        os.mkdir("c:\\BarrierV")
    except:
        pass
    os.system(f'copy {rtp} "C:\\BarrierV\\{rtp}"')
    open(f'C:\\BarrierV\\apikey.txt',"w").write(API_KEY)
    open(f'C:\\Users\\{os.getenv("username")}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\barrierv-rtp.bat',"w").write(f"start c:\\BarrierV\\{rtp}")
    os.system(f"start {rtp}")




def is_safe(filepath=None, url_to_scan=None, timeout=120):
    headers = {"x-apikey": API_KEY}

    if filepath:
        # VirusTotal API endpoint for file scanning
        file_scan_url = "https://www.virustotal.com/api/v3/files"

        # Open the file in binary mode and send it for scanning
        with open(filepath, "rb") as file:
            files = {"file": (filepath, file)}
            response = requests.post(file_scan_url, headers=headers, files=files)

        if response.status_code == 200:
            analysis_id = response.json()["data"]["id"]
        else:
            return f"Error scanning file. Status: {response.status_code}, Message: {response.text}"

    elif url_to_scan:
        # VirusTotal API endpoint for URL scanning
        url_scan_url = "https://www.virustotal.com/api/v3/urls"

        # POST request to scan the URL
        response = requests.post(url_scan_url, headers=headers, data={"url": url_to_scan})

        if response.status_code == 200:
            analysis_id = response.json()["data"]["id"]
        else:
            return f"Error scanning URL. Status: {response.status_code}, Message: {response.text}"

    else:
        return "You must provide either a filepath or a URL to scan."

    # Poll the analysis results with timeout
    result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            return "Timeout: Analysis took too long to complete."

        result_response = requests.get(result_url, headers=headers)
        if result_response.status_code == 200:
            analysis_result = result_response.json()
            status = analysis_result["data"]["attributes"]["status"]
            if status == "completed":
                break
        else:
            return f"Error fetching analysis results. Status: {result_response.status_code}, Message: {result_response.text}"

        # Provide feedback (status message)
        print("Waiting for analysis to complete...")
        time.sleep(5)  # Wait before polling again

    # Analyze the results to determine safety
    stats = analysis_result["data"]["attributes"]["stats"]
    harmless_count = stats.get("harmless", 0)
    malicious_count = stats.get("malicious", 0)
    total_votes = harmless_count + malicious_count

    if total_votes > 0:
        safe_percentage = (harmless_count / total_votes) * 100
        if safe_percentage >= 70:
            return "Safe"
        else:
            return "Not Safe"
    else:
        return "Safe"


@eel.expose
def newapi(apiholder):
    global API_KEY
    open("apikey.txt","w").write(apiholder)
    API_KEY = apiholder
@eel.expose
def scanfile():
    root = tkinter.Tk()
    root.withdraw()  # Hide the root window
    root.call('wm', 'attributes', '.', '-topmost', True)  # Bring file dialog to the front

    # Open the file dialog
    file = filedialog.askopenfilename(title="Select a file to scan")
    root.destroy()  # Close the root window

    if not file:
        return "No file selected"
    return is_safe(filepath=file)
@eel.expose
def github():
    webbrowser.open("https://github.com/MateuszKrawczynski")
@eel.expose
def urlscan(url):
    return is_safe(url_to_scan=url)


@eel.expose
def taskmgr():
    os.system("start taskmgr")

@eel.expose
def cclean():
    os.system("del /Q %temp%\\*")
    dirs = os.listdir(os.getenv("TEMP"))
    for el in dirs:
        try:
            shutil.rmtree(f"{os.getenv('TEMP')}\\{el}")
        except:
            pass
    dir_ = os.getcwd()
    os.chdir(os.getenv("TEMP"))
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")
    os.chdir("Downloads")
    os.system("del /Q *")
    os.chdir(dir_)
    os.system("cleanmgr.exe")
    return ""
@eel.expose
def sysscan():
    try:
        process = subprocess.run(
            ["sfc", "/scannow"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True  # On Windows, shell=True allows running built-in commands like `sfc`
        )
        if process.stdout == "You must be an administrator running a console session in order to use the sfc utility.":
            return "You must run BarrierV as administrator"
        return process.stdout
    except:
        return "Scan wasn't completed"
@eel.expose
def checkapi():
    if open("apikey.txt","r").read() == "":
        return "false"
    else:
        return "true"
@eel.expose
def safecopy():
    shutil.rmtree("temp-barrierv")
    os.mkdir("temp-barrierv")
    shutil.rmtree("copy-output")
    os.mkdir("copy-output")
    shutil.copytree("C:\\Users", "temp-barrierv\\Users", dirs_exist_ok=True)
    shutil.copytree("C:\\Program Files (x86)", "temp-barrierv\\Program Files (x86)", dirs_exist_ok=True)
    shutil.copytree("C:\\Program Files","temp-barrierv\\Program Files")
    shutil.make_archive("CopyOfPersonalData", 'zip', "temp-barrierv")
    os.system("move CopyOfPersonalData.zip copy-output\\CopyOfPersonalData.zip")
    os.system("explorer copy-output")

eel.init("web")
eel.start("index.html")
