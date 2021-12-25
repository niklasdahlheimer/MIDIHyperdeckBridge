"use strict";

// Websocket used to communicate with the Python server backend
var ws = new WebSocket("ws://" + location.host + "/ws");

// Global to keep track of whether we are filtering out state updates in the
// transcript area so that we only display the command/response when
// user-initiated
var allow_state_transcript = true;

// HyperDeck control elements on the HTML page
var loop = document.getElementById("loop");
var single = document.getElementById("single");
var speed = document.getElementById("speed");
var speed_val = document.getElementById("speed_val");
var state = document.getElementById("state");
var state_refresh = document.getElementById("state_refresh");
var clips = document.getElementById("clips");
var clips_refresh = document.getElementById("clips_refresh");
var record = document.getElementById("record");
var play = document.getElementById("play");
var stop = document.getElementById("stop");
var prev = document.getElementById("prev");
var next = document.getElementById("next");
var sent = document.getElementById("sent");
var received = document.getElementById("received");
var midi_inputs = document.getElementById("midi_inputs");

// Bind HTML elements to HyperDeck commands
speed.oninput = function () {
    speed_val.innerHTML = parseFloat(speed.value).toFixed(2);
};
record.onclick = function () {
    console.log("record clicked")
    var command = {
        "command": "record"
    };
    ws.send(JSON.stringify(command));
};
play.onclick = function () {
    var command = {
        "command": "play",
        "params": {
            "loop": loop.checked,
            "single": single.checked,
            "speed": speed.value
        }
    };
    ws.send(JSON.stringify(command));
};
stop.onclick = function () {
    var command = {
        "command": "stop"
    };
    ws.send(JSON.stringify(command));
};
prev.onclick = function () {
    var command = {
        "command": "clip_previous"
    };
    ws.send(JSON.stringify(command));
};
next.onclick = function () {
    var command = {
        "command": "clip_next"
    };
    ws.send(JSON.stringify(command));
};
state_refresh.onclick = function () {
    var command = {
        "command": "state_refresh"
    };
    ws.send(JSON.stringify(command));

    // Keep track of whether the user has initiated a state update, so we know
    // if we should show it in the transcript or not.
    allow_state_transcript = true;
};
clips.onchange = function () {
    var command = {
        "command": "clip_select",
        "params": {
            "id": clips.selectedIndex
        }
    };
    ws.send(JSON.stringify(command));
};
clips_refresh.onclick = function () {
    var command = {
        "command": "clip_refresh"
    };
    ws.send(JSON.stringify(command));
};
ws.onopen = function () {
    const command = {
        "command": "refresh"
    };
    ws.send(JSON.stringify(command));
};
midi_inputs.onchange = function () {
    console.log(midi_inputs)
    const selectInput = midi_inputs.options[midi_inputs.selectedIndex].text;

    const command = {
        "command": "midi_input_select",
        "params": {
            "name": selectInput
        }
    };
    ws.send(JSON.stringify(command));
};

// Websocket message parsing
ws.onmessage = function (message) {
    var data = JSON.parse(message.data);

    switch (data.response) {
        case "clip_count":
            clips.innerHTML = "";

            for (var i = 0; i < data.params["count"]; i++)
                clips.add(new Option("[--:--:--:--] - Clip " + i));

            break;

        case "clip_info":
            clips.options[data.params["id"] - 1].text = "[" + data.params["duration"] + "] " + data.params["name"];

            break;

        case "status":
            if (data.params["status"] !== undefined)
                state.innerHTML = data.params["status"] + " [" + data.params["timecode"] + "]";
            else
                state.innerHTML = "Unknown";

            break;

        case "transcript":
            // We periodically send transport info requests automatically
            // to the HyperDeck, so don't bother showing them to the user
            // unless this was a manual refresh request.
            var is_state_request = data.params["sent"][0] == "transport info";

            if (allow_state_transcript || !is_state_request) {
                sent.innerHTML = data.params["sent"].join("\n").trim();
                received.innerHTML = data.params["received"].join("\n").trim();

                allow_state_transcript = false;
            }
            break;
        case "clear_midi_inputs":
            console.log("requested clearing midi inputs");
            midi_inputs.innerHTML = "";

            break;
        case "midi_input":
            console.log("added midi input" + data.params["name"]);
            midi_inputs.add(new Option(data.params["name"]));

    }
    ;
};

// Initial control setup once the page is loaded
document.body.onload = function () {
    speed.value = 1.0;
    speed.oninput();
};
