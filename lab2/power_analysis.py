import csv
import os
from collections import defaultdict
from statistics import mean

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE, "result", "grade5", "power_results.csv")
OUTPUT = os.path.join(BASE, "result", "grade5", "power_summary.csv")


def main():
    times = defaultdict(list)
    checksums = set()

    with open(INPUT, newline="") as file:
        for row in csv.DictReader(file):
            T = int(row["processes"])
            times[T].append(float(row["time_seconds"]))
            checksums.add(int(row["checksum"]))

    if len(checksums) != 1:
        raise ValueError(
            f"Контрольные суммы различаются: {checksums}"
        )
    print(f"Контрольные суммы совпадают: {checksums.pop()}")

    summary = []
    for T, values in sorted(times.items()):
        if len(values) != 5:
            raise ValueError(
                f"Ожидалось 5 замеров, получено {len(values)} "
                f"для T={T}"
            )
        values.sort()
        summary.append({
            "processes": T,
            "average_time": mean(values[1:-1]),
        })

    baseline = summary[0]["average_time"]
    for row in summary:
        row["speedup"] = baseline / row["average_time"]
        row["efficiency"] = row["speedup"] / row["processes"]

    with open(OUTPUT, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "processes", "average_time",
                "speedup", "efficiency",
            ],
        )
        writer.writeheader()
        writer.writerows(summary)

    best = min(summary, key=lambda r: r["average_time"])
    print(f"Результаты сохранены в {OUTPUT}")
    print(
        f"Лучшее время: {best['average_time']:.4f} с "
        f"при T={best['processes']} "
        f"(ускорение {best['speedup']:.2f})"
    )


if __name__ == "__main__":
    main()
