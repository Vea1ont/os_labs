import csv
import os

import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(BASE, "result", "grade5", "power_summary.csv")

TICKS = [1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 48, 96]


def main():
    T, times, speedups = [], [], []

    with open(SUMMARY, newline="") as file:
        for row in csv.DictReader(file):
            T.append(int(row["processes"]))
            times.append(float(row["average_time"]))
            speedups.append(float(row["speedup"]))

    plt.figure(figsize=(12, 6))
    plt.plot(T, times, marker="o", markersize=4)
    plt.title("Возведение матрицы в степень: время")
    plt.xlabel("Число процессов")
    plt.ylabel("Время, с")
    plt.xticks(TICKS)
    plt.grid()
    out = os.path.join(BASE, "result", "grade5", "power_time.png")
    plt.savefig(out, dpi=150)
    print(f"График сохранён: {out}")

    plt.figure(figsize=(12, 6))
    plt.plot(T, speedups, marker="o", markersize=4,
             label="Ускорение")
    ideal = list(range(1, 25))
    plt.plot(ideal, ideal, "--", label="Идеальное ускорение")
    plt.axvline(8, linestyle=":", label="8 физических ядер")
    plt.axvline(12, linestyle=":",
                label="12 логических процессоров")
    plt.title("Возведение матрицы в степень: ускорение")
    plt.xlabel("Число процессов")
    plt.ylabel("Ускорение")
    plt.xticks(TICKS)
    plt.grid()
    plt.legend()
    out = os.path.join(BASE, "result", "grade5", "power_speedup.png")
    plt.savefig(out, dpi=150)
    print(f"График сохранён: {out}")


if __name__ == "__main__":
    main()
