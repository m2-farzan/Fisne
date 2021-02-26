var params = {}

function load_params() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            params = JSON.parse(this.responseText);
            document.getElementById("ip").innerHTML = params.ip;
            document.getElementById("latency").setAttribute("value", params.latency);
        }
    };
    request.open("GET", "/params", true);
    request.send();
}

function post_params() {
    params.latency = document.getElementById("latency").value;

    var request = new XMLHttpRequest();
    request.open("POST", "/params", true);
    request.send(JSON.stringify(params));
}

load_params();

