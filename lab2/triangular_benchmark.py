import csv
import os

from lab2.parallel import (
    run_triangular_multiplication,
    run_triangular_multiplication_dynamic,
)

PROCESSES = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    48, 96,
]
SIZES = [300, 500, 750]
REPEATS = 5

MODES = {
    "static": run_triangular_multiplication,
    "dynamic": run_triangular_multiplication_dynamic,
}

OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "result", "grade4", "triangular_results.csv",
)


def main():
    with open(OUTPUT, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "matrix_size", "mode", "processes",
            "repeat", "time_seconds", "checksum",
        ])

        for size in SIZES:
            for mode_name, runner in MODES.items():
                for T in PROCESSES:
                    for repeat in range(1, REPEATS + 1):
                        elapsed, checksum = runner(size, size, T)
                        writer.writerow([
                            size, mode_name, T,
                            repeat, elapsed, checksum,
                        ])
                        file.flush()
                        print(
                            f"Size: {size} | Mode: {mode_name} | "
                            f"T: {T} | Repeat: {repeat} | "
                            f"Time: {elapsed:.4f}s",
                            flush=True,
                        )


if __name__ == "__main__":
    main()
