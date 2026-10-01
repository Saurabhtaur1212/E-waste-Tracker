import random, time, requests
API="http://127.0.0.1:8000/api/bins"
BIN_ID="BIN-LAB-03"
while True:
    payload={
        "fill_level": random.randint(65,100),
        "temperature": round(random.uniform(26,38),1),
        "battery": random.randint(60,100)
    }
    try:
        r=requests.patch(f"{API}/{BIN_ID}/telemetry",json=payload,timeout=5)
        print(r.json())
    except Exception as e:
        print("Backend unavailable:",e)
    time.sleep(10)
