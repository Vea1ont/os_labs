import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from lab2.result_paths import (
    SUMMARY_CSV,
    EXECUTION_TIME_PNG,
    SPEEDUP_PNG
)


results = defaultdict(list)

with open(SUMMARY_CSV, newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        size = int(row["matrix_size"])
        T = int(row["processes"])

        average_time = float(row["average_time"])
        speedup = float(row["speedup"])

        results[size].append((T, average_time, speedup))


plt.figure(figsize=(12, 6))

for size, values in results.items():
    values.sort()

    T = [x[0] for x in values]
    times = [x[1] for x in values]

    plt.plot(T, times, marker="o", label=f"{size}x{size}")

plt.title("Время умножения матриц")
plt.xlabel("Количество процессов")
plt.ylabel("Время (секунды)")
plt.xticks([1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 48, 96])
plt.grid()
plt.legend()
plt.savefig(EXECUTION_TIME_PNG, dpi=150)



plt.figure(figsize=(12, 6))

for size, values in results.items():
    values.sort()

    T = [x[0] for x in values]
    speedups = [x[2] for x in values]

    plt.plot(T, speedups, marker="o", label=f"{size}x{size}")


ideal_T = list(range(1, 25))
plt.plot(ideal_T, ideal_T, "--", label="Идеальное ускорение")

plt.axvline(8, linestyle=":", label="8 физических ядер")
plt.axvline(12, linestyle=":", label="12 логических процессоров")

plt.title("Ускорение умножения матриц")
plt.xlabel("Количество процессов")
plt.ylabel("Ускорение")
plt.xticks([1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 48, 96])
plt.grid()
plt.legend()
plt.savefig(SPEEDUP_PNG, dpi=150)
plt.show()