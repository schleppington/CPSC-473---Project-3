var doGet = function (URL) {
    var xhr = new XMLHttpRequest(),
        events = document.getElementById("events");
     
    xhr.open("POST", URL, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) {
            return;
        }
         
        events.innerHTML = xhr.responseText;
    };
    xhr.send();
}
 
window.onload = function () {
    var refresh = document.getElementById("refresh"),     
    refresh.onclick = function () {
        doGet(document.URL);
        return false;
    };
};

//modified from exampled code from Professor Avery