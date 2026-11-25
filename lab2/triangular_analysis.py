import csv
import os
from collections import defaultdict
from statistics import mean

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE, "result", "grade4", "triangular_results.csv")
OUTPUT = os.path.join(BASE, "result", "grade4", "triangular_summary.csv")


def main():
    times = defaultdict(list)
    checksums = defaultdict(set)

    with open(INPUT, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            size = int(row["matrix_size"])
            mode = row["mode"]
            processes = int(row["processes"])
            times[(size, mode, processes)].append(
                float(row["time_seconds"])
            )
            checksums[(size, mode)].add(int(row["checksum"]))

    # Проверка 1: внутри одного режима контрольные суммы
    # не зависят от числа процессов
    for (size, mode), values in sorted(checksums.items()):
        if len(values) != 1:
            raise ValueError(
                f"Контрольные суммы различаются: {size} {mode}"
            )

    # Проверка 2: static и dynamic дают одинаковый результат
    sizes = sorted({size for size, _ in checksums})
    for size in sizes:
        static_sum = checksums[(size, "static")]
        dynamic_sum = checksums[(size, "dynamic")]
        if static_sum != dynamic_sum:
            raise ValueError(
                f"static != dynamic для размера {size}: "
                f"{static_sum} vs {dynamic_sum}"
            )
        print(
            f"Размер {size}: static == dynamic, "
            f"контрольная сумма {static_sum.pop()}"
        )

    summary = []
    for (size, mode, processes), values in sorted(times.items()):
        if len(values) != 5:
            raise ValueError(
                f"Ожидалось 5 замеров, получено {len(values)} "
                f"для {size}/{mode}/{processes}"
            )
        values.sort()
        summary.append({
            "matrix_size": size,
            "mode": mode,
            "processes": processes,
            "average_time": mean(values[1:-1]),
        })

    baseline = {
        (row["matrix_size"], row["mode"]): row["average_time"]
        for row in summary
        if row["processes"] == 1
    }
    for row in summary:
        key = (row["matrix_size"], row["mode"])
        row["speedup"] = baseline[key] / row["average_time"]

    with open(OUTPUT, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "matrix_size", "mode", "processes",
                "average_time", "speedup",
            ],
        )
        writer.writeheader()
        writer.writerows(summary)

    print(f"\nРезультаты сохранены в {OUTPUT}\n")

    for size in sizes:
        print(f"Матрица {size}x{size}:")
        for mode in ("static", "dynamic"):
            rows = [
                r for r in summary
                if r["matrix_size"] == size and r["mode"] == mode
            ]
            best = min(rows, key=lambda r: r["average_time"])
            print(
                f"  {mode:8s}: лучшее время "
                f"{best['average_time']:.4f} с "
                f"при T={best['processes']} "
                f"(ускорение {best['speedup']:.2f})"
            )
        pairs = {
            (r["processes"]): r["average_time"]
            for r in summary
            if r["matrix_size"] == size
        }


if __name__ == "__main__":
    main()
