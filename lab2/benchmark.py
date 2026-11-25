import csv

from lab2.parallel import run_multiplication
from lab2.result_paths import RESULTS_CSV

processes = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    48, 96
]

matrix_sizes = [300, 500, 750]
repeats = 5


def main():
    with open(RESULTS_CSV, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "matrix_size",
            "processes",
            "repeat",
            "time_seconds",
            "checksum"
        ])

        for size in matrix_sizes:
            for T in processes:
                for repeat in range(1, repeats + 1):

                    elapsed, checksum = run_multiplication(
                        size, size, size, T
                    )

                    writer.writerow([
                        size, T, repeat, elapsed, checksum
                    ])

                    file.flush()

                    print(
                        f"Size: {size} | "
                        f"Processes: {T} | "
                        f"Repeat: {repeat} | "
                        f"Time: {elapsed:.4f}s"
                    )


if __name__ == "__main__":
    main()