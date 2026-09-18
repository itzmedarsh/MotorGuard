import pandas as pd
import random

data=[]

for i in range(200):

    #Normal
    vib_rms= random.uniform(0.20,0.60)
    vib_std=random.uniform(0.05,0.20)
    vib_mean=random.uniform(0.10,0.40)

    current_rms=random.uniform(0.15,0.50)
    current_std=random.uniform(0.02,0.10)
    current_mean=random.uniform(0.1,0.40)

    rpm = random.uniform(900, 1000)
    temp_C = random.uniform(25, 45)

    data.append([
        vib_rms, vib_mean, vib_std,
        current_rms, current_mean, current_std,
        rpm, temp_C, "NORMAL"
    ])

    #overcurrent
    vib_rms = random.uniform(0.20, 0.70)
    vib_mean = random.uniform(0.10, 0.40)
    vib_std = random.uniform(0.05, 0.25)

    current_rms = random.uniform(1.50, 2.50)
    current_mean = random.uniform(1.40, 2.30)
    current_std = random.uniform(0.10, 0.40)

    rpm = random.uniform(800, 1000)
    temp_C = random.uniform(30, 55)

    data.append([
        vib_rms, vib_mean, vib_std,
        current_rms, current_mean, current_std,
        rpm, temp_C, "OVERCURRENT"
    ])

    #overheat
    vib_rms = random.uniform(0.20, 0.70)
    vib_mean = random.uniform(0.10, 0.40)
    vib_std = random.uniform(0.05, 0.25)

    current_rms = random.uniform(0.20, 0.70)
    current_mean = random.uniform(0.15, 0.60)
    current_std = random.uniform(0.02, 0.15)

    rpm = random.uniform(850, 1000)
    temp_C = random.uniform(60, 85)

    data.append([
        vib_rms, vib_mean, vib_std,
        current_rms, current_mean, current_std,
        rpm, temp_C, "OVERHEAT"
    ])

    #unbalance
    vib_rms = random.uniform(1.50, 2.50)
    vib_mean = random.uniform(0.50, 1.20)
    vib_std = random.uniform(0.50, 1.00)

    current_rms = random.uniform(0.30, 0.80)
    current_mean = random.uniform(0.20, 0.70)
    current_std = random.uniform(0.05, 0.20)

    rpm = random.uniform(700, 950)
    temp_C = random.uniform(30, 55)

    data.append([
        vib_rms, vib_mean, vib_std,
        current_rms, current_mean, current_std,
        rpm, temp_C, "UNBALANCE"
    ])

    #stopped
    vib_rms = random.uniform(0.00, 0.10)
    vib_mean = random.uniform(0.00, 0.05)
    vib_std = random.uniform(0.00, 0.05)

    current_rms = random.uniform(0.00, 0.10)
    current_mean = random.uniform(0.00, 0.08)
    current_std = random.uniform(0.00, 0.03)

    rpm = random.uniform(0, 20)
    temp_C = random.uniform(25, 45)

    data.append([
        vib_rms, vib_mean, vib_std,
        current_rms, current_mean, current_std,
        rpm, temp_C, "STOPPED"
    ])

    columns = [
    "vib_rms",
    "vib_mean",
    "vib_std",
    "current_rms",
    "current_mean",
    "current_std",
    "rpm",
    "temp_C",
    "status"
]
df = pd.DataFrame(data, columns=columns)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("dataset.csv", index=False)

print("Dataset created successfully!")
print("Total samples:", len(df))
print("\nClass distribution:")
print(df["status"].value_counts())
    
    
