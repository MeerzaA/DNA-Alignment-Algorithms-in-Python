import os
import pandas as pd
import subprocess
import re

input_dir = "datapoints"
basic_dir = "basic"
eff_dir = "efficient"

os.makedirs(basic_dir, exist_ok=True)
os.makedirs(eff_dir, exist_ok=True)

# Optional: rename in1.txt → in01.txt
for file in os.listdir(input_dir):
    match = re.match(r"in(\d+)\.txt", file)
    if match:
        num = int(match.group(1))
        new_name = f"in{num:02d}.txt"
        old_path = os.path.join(input_dir, file)
        new_path = os.path.join(input_dir, new_name)
        if file != new_name:
            os.rename(old_path, new_path)
            print(f"Renamed {file} → {new_name}")

# Extract number for sorting
def extract_number(file):
    match = re.match(r"in(\d+)_bas_out\.txt", file)
    return int(match.group(1)) if match else float('inf')

results = []

# Process input files sorted numerically
for file in sorted(os.listdir(input_dir), key=lambda f: int(re.search(r"in(\d+)", f).group(1))):
    if not file.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, file)
    base_name = os.path.splitext(file)[0]  # e.g., "in01"

    basic_output = os.path.join(basic_dir, f"{base_name}_bas_out.txt")
    eff_output = os.path.join(eff_dir, f"{base_name}_eff_out.txt")

    # Run both programs
    subprocess.run(["python", "basic_3.py", input_path, basic_output])
    subprocess.run(["python", "efficient_3.py", input_path, eff_output])

    # Read outputs
    with open(basic_output) as f:
        basic = [line.strip() for line in f.readlines()]
    with open(eff_output) as f:
        eff = [line.strip() for line in f.readlines()]

    # Extract alignment size
    size = len(basic[1]) + len(basic[2])

    results.append({
        "file": base_name,
        "problem_size": size,
        "basic_time": float(basic[3]),
        "basic_mem": float(basic[4]),
        "eff_time": float(eff[3]),
        "eff_mem": float(eff[4]),
    })

# Export summary
df = pd.DataFrame(results)
df.to_csv("summary_data.csv", index=False)
print("✅ summary_data.csv generated in numeric order.")
