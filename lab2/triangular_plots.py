import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(BASE, "result", "grade4", "triangular_summary.csv")
IPC = os.path.join(BASE, "result", "grade4", "ipc_transfer.csv")
RESULTS = os.path.join(BASE, "result", "grade4", "triangular_results.csv")

TICKS = [1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 48, 96]


def plot_static_vs_dynamic():
    data = defaultdict(list)

    with open(SUMMARY, newline="") as file:
        for row in csv.DictReader(file):
            size = int(row["matrix_size"])
            mode = row["mode"]
            data[(size, mode)].append((
                int(row["processes"]),
                float(row["average_time"]),
            ))

    sizes = sorted({size for size, _ in data})

    fig, axes = plt.subplots(1, len(sizes), figsize=(18, 5), sharex=True)

    for ax, size in zip(axes, sizes):
        for mode, label in (("static", "Статическое"),
                            ("dynamic", "Динамическое")):
            values = sorted(data[(size, mode)])
            T = [v[0] for v in values]
            times = [v[1] for v in values]
            ax.plot(T, times, marker="o", markersize=3, label=label)

        ax.set_title(f"Матрица {size}x{size}")
        ax.set_xlabel("Число процессов")
        ax.set_ylabel("Время, с")
        ax.set_xticks(TICKS)
        ax.tick_params(axis="x", rotation=45)
        ax.grid()
        ax.legend()

    fig.suptitle(
        "Треугольная матрица: статическое и динамическое "
        "распределение строк"
    )
    fig.tight_layout()
    out = os.path.join(BASE, "result", "grade4", "triangular_static_dynamic.png")
    fig.savefig(out, dpi=150)
    print(f"График сохранён: {out}")


def plot_ipc_transfer():
    transfer = defaultdict(list)
    mult_time = defaultdict(dict)

    with open(IPC, newline="") as file:
        for row in csv.DictReader(file):
            size = int(row["matrix_size"])
            transfer[size].append(float(row["transfer_seconds"]))

    with open(SUMMARY, newline="") as file:
        for row in csv.DictReader(file):
            if row["mode"] == "dynamic" and row["processes"] == "1":
                size = int(row["matrix_size"])
                mult_time[size] = float(row["average_time"])

    sizes = sorted(transfer)
    transfer_avg = []
    for size in sizes:
        values = sorted(transfer[size])
        transfer_avg.append(
            sum(values[1:-1]) / len(values[1:-1])
        )
    mult = [mult_time[size] for size in sizes]

    x = range(len(sizes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar([i - width / 2 for i in x], transfer_avg, width,
           label="Передача данных (Queue)")
    ax.bar([i + width / 2 for i in x], mult, width,
           label="Умножение (1 процесс)")

    ax.set_title("Время передачи данных и время умножения")
    ax.set_xlabel("Размер матрицы")
    ax.set_ylabel("Время, с")
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{s}x{s}" for s in sizes])
    ax.grid(axis="y")
    ax.legend()

    fig.tight_layout()
    out = os.path.join(BASE, "result", "grade4", "ipc_transfer.png")
    fig.savefig(out, dpi=150)
    print(f"График сохранён: {out}")


if __name__ == "__main__":
    plot_static_vs_dynamic()
    plot_ipc_transfer()
