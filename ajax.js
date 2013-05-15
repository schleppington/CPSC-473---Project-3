var doGet = function (URL) {
    var xhr = new XMLHttpRequest(),
        events = document.getElementById("events");
     
    xhr.open("GET", URL+"/ajax", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) {
            return;
        }
         
        events.innerHTML = xhr.responseText;
	setTimeout('doGet(document.URL)', 1000);
    };
    xhr.send();
}
 
window.onload = function () {
    var refresh = document.getElementById("refresh");
	setTimeout('doGet(document.URL)', 1000);
};

//modified from example code from Professor Avery