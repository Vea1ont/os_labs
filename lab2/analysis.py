import csv
from collections import defaultdict
from statistics import mean
from lab2.result_paths import RESULTS_CSV, SUMMARY_CSV

def main():
    results = defaultdict(list)
    checksums = defaultdict(set)

    with open(RESULTS_CSV, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            size = int(row["matrix_size"])
            processes = int(row["processes"])
            elapsed = float(row["time_seconds"])
            checksum = int(row["checksum"])

            results[(size, processes)].append(elapsed)
            checksums[size].add(checksum)

    summary = []

    for (size, processes), times in sorted(results.items()):
        if len(times) != 5:
            raise ValueError(
                f"Ожидалось 5 замеров, получено {len(times)}"
            )

        times.sort()
        average = mean(times[1:-1])

        summary.append({
            "matrix_size": size,
            "processes": processes,
            "average_time": average
        })

    baseline = {
        row["matrix_size"]: row["average_time"]
        for row in summary
        if row["processes"] == 1
    }

    for row in summary:
        speedup = (
            baseline[row["matrix_size"]] / row["average_time"]
        )

        row["speedup"] = speedup
        row["efficiency"] = speedup / row["processes"]

    with open(SUMMARY_CSV, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "matrix_size",
                "processes",
                "average_time",
                "speedup",
                "efficiency"
            ]
        )

        writer.writeheader()
        writer.writerows(summary)

    print("Результаты сохранены в summary.csv")

    for size in baseline:
        best = min(
            (row for row in summary
             if row["matrix_size"] == size),
            key=lambda row: row["average_time"]
        )

        print(
            f"\nМатрица {size}x{size}:"
            f"\nЛучшее время: {best['average_time']:.4f} сек"
            f"\nПроцессов: {best['processes']}"
            f"\nУскорение: {best['speedup']:.2f}"
            f"\nЭффективность: {best['efficiency']:.2%}"
        )

    if any(len(values) != 1 for values in checksums.values()):
        raise ValueError("Контрольные суммы различаются!")

    print("\nКонтрольные суммы для каждого размера совпадают.")


if __name__ == "__main__":
    main()