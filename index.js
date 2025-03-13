document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "10.0.0.65";   // the IP address of your Raspberry PI

// Send data to the Raspberry Pi
function send_data(command) {
    const net = require('net');

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('Connected to server');
        client.write(command + "\r\n");
    });

    client.on('data', (data) => {
        let response = data.toString().trim();
        console.log("Server Response:", response);

        if (response.startsWith("Distance")) {
            document.getElementById("distance").innerHTML = response.split(": ")[1];  // Display the distance
        } else if (response.startsWith("Direction")) {
            document.getElementById("direction").innerHTML = response.split(": ")[1];  // Display the direction
        }
    });

    client.on('end', () => {
        console.log('Disconnected from server');
    });
}

// Update key color and send data on key press (w, a, s, d)
function updateKey(e) {
    e = e || window.event;

    if (e.keyCode == '38') { // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("forward");
    }
    else if (e.keyCode == '40') { // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("backward");
    }
    else if (e.keyCode == '37') { // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("left");
    }
    else if (e.keyCode == '39') { // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("right");
    }
    else if (e.keyCode == '32') { // stop
        document.getElementById("stopbutt").style.color = "green";
        send_data("stop");
    }
    else if (e.keyCode == '13') { // distance
        document.getElementById("distancebutt").style.color = "green";
        send_data("distance");
    }
}

// Reset arrow colors when key is released
function resetKey(e) {
    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
    document.getElementById("stopbutt").style.color = "black";
    document.getElementById("distancebutt").style.color = "black";
}

// Clickable arrows 
function setupClickableArrows() {
    document.getElementById("upArrow").onclick = function() {
        document.getElementById("upArrow").style.color = "green";
        send_data("forward");  // forward
    };
    document.getElementById("downArrow").onclick = function() {
        document.getElementById("downArrow").style.color = "green";
        send_data("backward");  //backward
    };
    document.getElementById("leftArrow").onclick = function() {
        document.getElementById("leftArrow").style.color = "green";
        send_data("left");  // left
    };
    document.getElementById("rightArrow").onclick = function() {
        document.getElementById("rightArrow").style.color = "green";
        send_data("right");  s// right
    };
    document.getElementById("stopbutt").onclick = function() {
        document.getElementById("stopbutt").style.color = "green";
        send_data("stop");  // stop
    };
}

/* // Request ultrasonic data periodically
setInterval(function() {
    send_data("distance");
}, 1000);
 */
// Initialize clickable arrows when the page loads
window.onload = function() {
    setupClickableArrows();
};
