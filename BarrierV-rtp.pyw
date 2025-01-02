from tkinter import *
import os
import requests
import base64
import time
tmp = os.listdir(f"c:\\Users\\{os.getenv('username')}\\Downloads")
API_KEY = open("c:\\BarrierV\\apikey.txt","r").read()
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

while True:
    cur = os.listdir(f"c:\\Users\\{os.getenv('username')}\\Downloads")
    if cur != tmp:
        for file in cur:
            if not file in tmp:
                if not (file.endswith(".tmp") or file.endswith(".crdownload")):
                        pop = Tk()
                        pop.title("BarrierV")
                        pop.call('wm', 'attributes', '.', '-topmost', True)
                        tmp = cur
                        Label(pop,text="BarrierV Real Time Protection",font=("arial",15,"normal")).grid(row=0,column=0)
                        Label(pop,text="New file in downloads detected").grid(row=1,column=0)
                        Label(pop,text=file).grid(row=2,column=0)
                        actions = Canvas(pop)
                        actions.grid(row=3,column=0)
                        def scan():
                            res = is_safe(filepath=f"c:\\Users\\{os.getenv('username')}\\Downloads\\{file}")
                            if res == "Safe":
                                pop.destroy()
                                new = Tk()
                                new.title("BarrierV")
                                Label(new,text="File is safe,\nno worries!",font=("arial",30,"normal"),fg="green").grid(row=0,column=0)
                                new.mainloop()
                            elif res == "Not Safe":
                                new = Tk()
                                new.title("BarrierV")
                                Label(new, text="File isn't safe", font=("arial", 30, "normal"), fg="red").grid(row=0, column=0)
                                new.mainloop()
                        def delete():
                            pop.destroy()
                            ask = Tk()
                            ask.title("BarrierV")
                            def rem():
                                ask.destroy()
                                os.remove(f"c:\\Users\\{os.getenv('username')}\\Downloads\\{file}")
                            Label(ask,text="Are you sure you want to delete this file?").grid(row=0,column=0)
                            Button(ask,text="Yes", command=lambda: rem()).grid(row=1,column=0)
                            Button(ask,text="No", command= lambda: ask.destroy()).grid(row=2,column=0)
                            ask.mainloop()

                        Button(actions,text="Scan the file",command=lambda: scan()).grid(row=0,column=0)
                        Button(actions,text="Delete the file", command=lambda: delete()).grid(row=0,column=1,padx=10)
                        Button(actions,text="Ignore" , command=lambda: pop.destroy()).grid(row=0,column=2,padx=10)
                        pop.mainloop()
                        break