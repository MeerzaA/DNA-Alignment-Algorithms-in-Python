import os
import re
import pandas as pd
import matplotlib.pyplot as plt

basic_dir = "basic"
eff_dir = "efficient"
results = []

# Extract input number for numeric sorting
def extract_input_number(filename):
    match = re.search(r"in(\d+)_bas_out\.txt", filename)
    if not match:
        print(f"⚠️ Could not parse input number from filename: {filename}")
    return int(match.group(1)) if match else float('inf')

# Collect and parse data
for file in sorted(os.listdir(basic_dir), key=extract_input_number):
    if not file.endswith("_bas_out.txt"):
        continue

    base_name = file.replace("_bas_out.txt", "")
    basic_path = os.path.join(basic_dir, file)
    eff_path = os.path.join(eff_dir, f"{base_name}_eff_out.txt")

    if not os.path.exists(eff_path):
        print(f"⚠️ Missing matching efficient file for {file}")
        continue

    with open(basic_path) as f:
        basic_lines = [line.strip() for line in f.readlines()]
    with open(eff_path) as f:
        eff_lines = [line.strip() for line in f.readlines()]

    if len(basic_lines) < 5 or len(eff_lines) < 5:
        print(f"❌ Skipping {file} due to incomplete output")
        continue

    aligned_x = basic_lines[1]
    aligned_y = basic_lines[2]
    # Estimate problem size by counting non-gap characters
    size_x = len(aligned_x.replace("_", ""))
    size_y = len(aligned_y.replace("_", ""))
    problem_size = size_x + size_y

    results.append({
        "file": base_name,
        "problem_size": problem_size,
        "basic_time": float(basic_lines[3]),
        "basic_mem": float(basic_lines[4]),
        "eff_time": float(eff_lines[3]),
        "eff_mem": float(eff_lines[4]),
    })

# Output DataFrame
df = pd.DataFrame(results)
df.to_csv("summary_data_v2.csv", index=False)

if df.empty:
    print("❌ No data collected. Check filenames and folder contents.")
    exit()

# Plot: CPU Time vs Problem Size
plt.figure()
plt.plot(df["problem_size"], df["basic_time"], linewidth=2, label="Basic")
plt.plot(df["problem_size"], df["eff_time"], linewidth=2, label="Efficient")
plt.title("CPU Time vs Problem Size")
plt.xlabel("Problem Size (m + n)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("time_vs_size.png")

# Plot: Memory Usage vs Problem Size
plt.figure()
plt.plot(df["problem_size"], df["basic_mem"], linewidth=2, label="Basic")
plt.plot(df["problem_size"], df["eff_mem"], linewidth=2, label="Efficient")
plt.title("Memoery Usage vs Problem Size")
plt.xlabel("Problem Size (m + n)")
plt.ylabel("Memory (KB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("memory_vs_size.png")

print("✅ summary_data_v2.csv, time_vs_size.png, and memory_vs_size.png generated.")