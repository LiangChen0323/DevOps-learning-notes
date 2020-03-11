import os
import glob
import json
import shutil
import math
try:
    os.mkdir("./processed")
except OSError:
    print("processd directory already exists")

# receipts = glob.glob("./new/receipt-[0-9]*.json")

subtotal = 0.0

for path in glob.iglob("./new/receipt-[0-9]*.json"):
    with open(path) as f:
        content = json.load(f)
        subtotal += float(content["value"])
    name = path.split("/")[-1]
    destination = path.replace("new", "processed")
    shutil.move(path, destination)
    print(f"move {path} to {destination}")

print(f"Receipt subtotal: ${round(subtotal,2)}"
