const temperatureElement = document.getElementById("temperature");
const currentElement = document.getElementById("current");
const rpmElement = document.getElementById("rpm");
const vibrationElement = document.getElementById("vibration");

const connectionDot = document.getElementById("connection-dot");
const connectionText = document.getElementById("connection-text");

const predictionElement = document.getElementById("prediction");
const confidenceElement = document.getElementById("confidence");
const updatedElement = document.getElementById("updated");

const statusCard = document.getElementById("statusCard");
const motorStatus = document.getElementById("motorStatus");
const statusDescription = document.getElementById("statusDescription");
const statusIcon = document.getElementById("statusIcon");

const vibrationGaugeValue =
    document.getElementById("vibrationGaugeValue");

const currentGaugeValue =
    document.getElementById("currentGaugeValue");

const vibrationNeedle =
    document.getElementById("vibrationNeedle");

const currentNeedle =
    document.getElementById("currentNeedle");

let lastDataReceived = 0;
let previousFault = "NORMAL";
function saveFault(fault, vibration, current, temperature, rpm) {

    const history = JSON.parse(
        localStorage.getItem("motorFaultHistory") || "[]"
    );


    const now = new Date();

    const time =
        now.toLocaleDateString() +
        " " +
        now.toLocaleTimeString();


    history.push({

        time: time,

        fault: fault,

        vibration: Number(vibration).toFixed(2),

        current: Number(current).toFixed(2),

        temperature: Number(temperature).toFixed(1),

        rpm: rpm

    });


    /*
       Keep latest 100 events
    */

    if (history.length > 100) {
        history.shift();
    }


    localStorage.setItem(
        "motorFaultHistory",
        JSON.stringify(history)
    );

}

/* =================================
   UPDATE GAUGE
================================= */

function updateGauge(value, needle, valueElement) {
    const limitedValue = Math.max(0, Math.min(2, Number(value) || 0));

    // 0.0 = LEFT
    // 1.0 = TOP
    // 2.0 = RIGHT
    const angle = -180 + (limitedValue / 2) * 180;

    needle.style.transform = `rotate(${angle}deg)`;
    valueElement.textContent = limitedValue.toFixed(2);
}


/* =================================
   UPDATE MOTOR STATUS
================================= */

function updateMotorStatus(prediction, vibration, current, temperature, rpm) {

    const fault = prediction;

    motorStatus.textContent = fault;
    predictionElement.textContent = fault;

    // Normal
    if (fault === "NORMAL") {

        statusCard.className = "status-card normal";
        statusIcon.textContent = "✓";

        statusDescription.textContent =
            "Motor operating within normal parameters";

    }

    // Fault
    else {

        statusCard.className = "status-card danger";
        statusIcon.textContent = "!";

        statusDescription.textContent =
            "AI detected: " + fault;

        // Save to fault history
        if (fault !== previousFault) {
            saveFault(
                fault,
                vibration,
                current,
                temperature,
                rpm
            );
        }
    }

    previousFault = fault;
}

/* =================================
   WEBSOCKET
================================= */

const socketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const socket = new WebSocket(
    `${socketProtocol}://${window.location.host}/ws`
);

const connectionText = document.getElementById("connection-text");

socket.onopen = () => {
    connectionText.textContent = "SYSTEM ONLINE";
};

socket.onclose = () => {
    connectionText.textContent = "SYSTEM OFFLINE";
};

socket.onerror = () => {
    connectionText.textContent = "SYSTEM OFFLINE";
};

/* =================================
   CONVERT VALUES TO NUMBERS
================================= */

const temperature = Number(data.temperature);
const current = Number(data.current);
const rpm = Number(data.rpm);
const vibration = Number(data.vibration);


/* =================================
   CONNECTION
================================= */

if (connectionDot) {

    connectionDot.style.background = "";

}

if (connectionText) {

    connectionText.textContent =
        "ESP32 Connected";

}


/* =================================
   SENSOR VALUES
================================= */

if (temperatureElement) {

    temperatureElement.textContent =
        temperature.toFixed(1);

}


if (currentElement) {

    currentElement.textContent =
        current.toFixed(2);

}


if (rpmElement) {

    rpmElement.textContent =
        rpm;

}


if (vibrationElement) {

    vibrationElement.textContent =
        vibration.toFixed(2);

}


/* =================================
   GAUGES
================================= */

updateGauge(
    vibration,
    vibrationNeedle,
    vibrationGaugeValue
);


updateGauge(
    current,
    currentNeedle,
    currentGaugeValue
);


/* =================================
   MOTOR STATUS
================================= */

updateMotorStatus(
    data.prediction,
    data.vibration,
    data.current,
    data.temperature,
    data.rpm
);


/* =================================
   AI PREDICTION
================================= */

if (
    predictionElement &&
    data.prediction
) {

    predictionElement.textContent =
        data.prediction;

}


/* =================================
   LAST UPDATED
================================= */

if (updatedElement) {

    updatedElement.textContent =
        "Just now";

}

};


/* =================================
   CONNECTION TIMEOUT
================================= */

setInterval(() => {

    if (Date.now() - lastDataReceived > 3000) {

        if (connectionDot) {

            connectionDot.style.background =
                "#777";

        }

        if (connectionText) {

            connectionText.textContent =
                "ESP32 Disconnected";

            temperatureElement.textContent = "0.0";
            currentElement.textContent = "0.00";
            rpmElement.textContent = "0";
            vibrationElement.textContent = "0.00";

            updateGauge(0, vibrationNeedle, vibrationGaugeValue);
            updateGauge(0, currentNeedle, currentGaugeValue);

            motorStatus.textContent = "OFFLINE";
            statusDescription.textContent = "ESP32 is disconnected";
            statusIcon.textContent = "✕";
        }

    }

}, 1000);


/* =================================
   ERROR
================================= */

socket.onerror = () => {

    console.log("❌ WebSocket error");

    if (connectionDot) {

        connectionDot.style.background =
            "#777";

    }

    if (connectionText) {

        connectionText.textContent =
            "ESP32 Disconnected";

    }

};


/* =================================
   CLOSED
================================= */

socket.onclose = () => {

    console.log("❌ WebSocket disconnected");

    if (connectionDot) {

        connectionDot.style.background =
            "#777";

    }

    if (connectionText) {

        connectionText.textContent =
            "ESP32 Disconnected";

    }

};
