function boot(){
    eel.checkapi()((response) => {
        if (response == "false"){
            document.getElementById('mid') .innerHTML = `<center> <br><br><br><br><input style="width:90%;" id="apiholder" type="text" placeholder="Insert your VirusTotal api key" required/><br><br><br><button onclick="_newapi()">Set key</button></center>`;
        }
    });
    
}
function _newapi(){
    eel.newapi(document.getElementById('apiholder').value);
    document.getElementById('mid').innerHTML = "<center><h1>Your new api key is loaded</h1></center>";
}
function setapi(){
    document.getElementById('mid') .innerHTML = `<center> <br><br><br><br><input style="width:90%;" id="apiholder" type="text" placeholder="Insert your VirusTotal api key" required/><br><br><br><button onclick="_newapi()">Set key</button></center>`;
}
function scanfile(){
    document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1>Scanning...</h1></center>'
    eel.scanfile()((response) => {
        if (response == "Safe"){
            document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1 style="color:limegreen;">Scanned file is</h1><br><br><h1 style="color:limegreen;">SAFE</h1></center>';
        }
        else if (response == "Not Safe"){
            document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1 style="color:red;">Scanned file is</h1><br><br><h1 style="color:red;">NOT SAFE</h1></center>';
        }
        else if (response == "Not Enough Data to Determine Safety"){
            document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1>Safety of scanned file is unknown</h1><br><br><h1>Not Enough Data to Determine Safety</h1></center>';
        }
    });
}
function github(){
    eel.github();
}
function webscan(){
    document.getElementById('mid').innerHTML = '<center><br><br><br><br><input style="width:90%;" id="urlholder" type="text" placeholder="Enter the URL" required/><br><br><button onclick="_webscan()">Scan</button></center>';
}
function _webscan(){
    let url = document.getElementById('urlholder').value;
    document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1>Scanning...</h1></center>';
    eel.urlscan(url)((response) => {
        if (response == "Safe"){
            document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1 style="color:limegreen;">Scanned website is</h1><br><br><h1 style="color:limegreen;">SAFE</h1></center>';
        }
        else if (response == "Not Safe"){
            document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1 style="color:red;">Scanned website is</h1><br><br><h1 style="color:red;">NOT SAFE</h1></center>';
        }
        else if (response == "Not Enough Data to Determine Safety"){
            document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1>Safety of scanned website is unknown</h1><br><br><h1>Not Enough Data to Determine Safety</h1></center>';
        }
    });
}
function taskmgr(){
    eel.taskmgr();
}
function cclean(){
    document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1>Cleaning...</h1></center>';
    eel.cclean()((response) => {
        document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1>Cleaned!</h1></center>';
    });
}
function sysscan(){
    document.getElementById('mid').innerHTML = '<center><br><br><br><br><h1>Scanning...</h1><br><h1>15-20 minutes</h1></center>';
    eel.sysscan()((response) => {
        document.getElementById('mid').innerHTML = `<center><h2>${response}</h2></center>`;
    });
}
function safecopy(){
    document.getElementById('mid').innerHTML = '<center><h1>Your files are copying...</h1><br><h1>File explorer will open in the directiory the copy is</h1><br><h1>It will take some time and disk space</jh1></center>';
    eel.safecopy()((response) => {
        document.getElementById('mid').innerHTML = '<center><h1>Your copy is ready</h1><br><h1>Take the files and save them somewhere</h1></center>'
    });
}