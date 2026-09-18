import asyncio
import json
import math
import os
from collections import deque

import joblib
from aiohttp import web

# ================= MODEL =================

model = joblib.load("modelDecision.pkl")

# ================= CLIENTS =================

clients = set()

# ================= SENSOR BUFFERS =================

vibration_buffer = deque(maxlen=10)
current_buffer = deque(maxlen=10)


# ================= FEATURES =================

def calculate_features():

    if len(vibration_buffer) < 10:
        return None

    if len(current_buffer) < 10:
        return None

    vib = list(vibration_buffer)
    cur = list(current_buffer)

    # Vibration
    vib_mean = sum(vib) / len(vib)

    vib_rms = math.sqrt(
        sum(x * x for x in vib) / len(vib)
    )

    vib_std = math.sqrt(
        sum((x - vib_mean) ** 2 for x in vib) / len(vib)
    )

    # Current
    current_mean = sum(cur) / len(cur)

    current_rms = math.sqrt(
        sum(x * x for x in cur) / len(cur)
    )

    current_std = math.sqrt(
        sum((x - current_mean) ** 2 for x in cur) / len(cur)
    )

    return (
        vib_rms,
        vib_mean,
        vib_std,
        current_rms,
        current_mean,
        current_std
    )


# ================= ESP32 DATA =================

async def receive_esp32(request):

    try:

        data = await request.json()

        temperature = float(data["temperature"])
        current = float(data["current"])
        rpm = float(data["rpm"])
        vibration = float(data["vibration"])

        vibration_buffer.append(vibration)
        current_buffer.append(current)

        features = calculate_features()

        if features is None:

            prediction = "CALIBRATING"

        else:

            (
                vib_rms,
                vib_mean,
                vib_std,
                current_rms,
                current_mean,
                current_std
            ) = features

            model_input = [[
                vib_rms,
                vib_mean,
                vib_std,
                current_rms,
                current_mean,
                current_std,
                rpm,
                temperature
            ]]

            prediction = model.predict(model_input)[0]

        dashboard_data = {
            "temperature": round(temperature, 1),
            "current": round(current, 2),
            "rpm": round(rpm),
            "vibration": round(vibration, 2),
            "prediction": str(prediction)
        }

        if features is not None:

            dashboard_data.update({
                "vib_rms": round(vib_rms, 3),
                "vib_mean": round(vib_mean, 3),
                "vib_std": round(vib_std, 3),
                "current_rms": round(current_rms, 3),
                "current_mean": round(current_mean, 3),
                "current_std": round(current_std, 3)
            })

        print(
            f"Temp: {temperature:.1f} | "
            f"Current: {current:.2f} | "
            f"RPM: {rpm:.0f} | "
            f"Vibration: {vibration:.2f} | "
            f"Prediction: {prediction}"
        )

        # Send to all dashboards
        if clients:

            message = json.dumps(dashboard_data)

            await asyncio.gather(
                *(client.send_str(message) for client in clients),
                return_exceptions=True
            )

        return web.json_response({
            "status": "ok",
            "prediction": str(prediction)
        })

    except Exception as e:

        print("ESP32 ERROR:", e)

        return web.json_response(
            {
                "status": "error",
                "message": str(e)
            },
            status=500
        )


# ================= WEBSOCKET =================

async def websocket_handler(request):

    ws = web.WebSocketResponse()

    await ws.prepare(request)

    clients.add(ws)

    print("Dashboard connected!")

    try:

        async for msg in ws:

            pass

    finally:

        clients.discard(ws)

        print("Dashboard disconnected!")

    return ws


# ================= HEALTH CHECK =================

async def health(request):

    return web.json_response({
        "status": "MotorGuard online"
    })


# ================= STATIC FILES =================

async def index(request):

    return web.FileResponse("web.html")


# ================= MAIN =================

async def main():

    app = web.Application()

    # ESP32
    app.router.add_post(
        "/data",
        receive_esp32
    )

    # Dashboard WebSocket
    app.router.add_get(
        "/ws",
        websocket_handler
    )

    # Health
    app.router.add_get(
        "/health",
        health
    )

    # Dashboard pages
    app.router.add_get(
        "/",
        index
    )

    app.router.add_static(
        "/",
        ".",
        show_index=False
    )

    # Render provides PORT
    port = int(os.environ.get("PORT", 5001))

    print("================================")
    print("MotorGuard Cloud Server")
    print("================================")
    print(f"Listening on port: {port}")
    print("ESP32 endpoint: /data")
    print("WebSocket endpoint: /ws")
    print("Health endpoint: /health")
    print("================================")

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    await asyncio.Future()


asyncio.run(main())