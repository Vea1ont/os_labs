import csv
import os

from lab2.power import run_power

N = 500
P = 3
PROCESSES = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    48, 96,
]
REPEATS = 5

OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "result", "grade5", "power_results.csv",
)


def main():
    with open(OUTPUT, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "n", "p", "processes", "repeat",
            "time_seconds", "checksum",
        ])

        for T in PROCESSES:
            for repeat in range(1, REPEATS + 1):
                elapsed, checksum = run_power(N, P, T)
                writer.writerow([N, P, T, repeat, elapsed, checksum])
                file.flush()
                print(
                    f"n={N} p={P} | T: {T} | "
                    f"Repeat: {repeat} | Time: {elapsed:.4f}s",
                    flush=True,
                )


if __name__ == "__main__":
    main()
