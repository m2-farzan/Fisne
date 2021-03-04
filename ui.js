var params = {}
keys = ['latency', 'jitter', 'loss', 'rate', 'P', 'E_B', 'rho', 'P_isol', 'E_GB']

function load_params() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            params = JSON.parse(this.responseText);
            document.getElementById("dist").value = params.dist;
            document.getElementById("loss_model").value = params.loss_model;
            document.getElementById("ip").innerHTML = params.ip;
            for (i=0; i<keys.length; i++)
            {
                document.getElementById(keys[i]).setAttribute("value", params[keys[i]]);
            }
            loss_model_changed();
        }
    };
    request.open("GET", "/params", true);
    request.send();
}

function post_params() {
    
    params.dist = document.getElementById("dist").value;
    params.loss_model = document.getElementById("loss_model").value;
    for (i=0; i<keys.length; i++)
    {
        params[keys[i]] = document.getElementById(keys[i]).value;
    }
    var request = new XMLHttpRequest();
    request.open("POST", "/params", true);
    request.send(JSON.stringify(params));
}

function loss_model_changed() {
    if (document.getElementById("loss_model").value == 'random') {
        document.getElementById("loss-random-options").setAttribute("style", "display: contents;")
        document.getElementById("loss-gi-options").setAttribute("style", "display: none;")
    }
    else if (document.getElementById("loss_model").value == 'gi') {
        document.getElementById("loss-random-options").setAttribute("style", "display: none;")
        document.getElementById("loss-gi-options").setAttribute("style", "display: contents;")
    }
}

load_params();