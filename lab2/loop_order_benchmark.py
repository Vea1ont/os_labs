import csv
import time
from statistics import mean

from lab2.matrix import (
    checksum,
    generate_matrices,
    multiply_matrices,
    multiply_matrices_ikj,
)
from lab2.result_paths import LOOP_ORDER_CSV

def main():
    n = 750
    m = 750
    k = 750
    repeats = 5

    A, B = generate_matrices(n, m, k, seed=42)

    implementations = {
        "i_j_r": multiply_matrices,
        "i_r_j": multiply_matrices_ikj
    }

    results = {
        "i_j_r": [],
        "i_r_j": []
    }

    with open(LOOP_ORDER_CSV, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["order", "repeat", "time", "checksum"])

        for repeat in range(1, repeats + 1):

            outputs = {}

            order = list(implementations.items())

            if repeat % 2 == 0:
                order.reverse()

            for name, func in order:

                start = time.perf_counter()

                C = func(A, B, n, m, k)

                elapsed = time.perf_counter() - start

                outputs[name] = C
                results[name].append(elapsed)

                writer.writerow([
                    name,
                    repeat,
                    elapsed,
                    checksum(C)
                ])

                file.flush()

                print(
                    f"{name}: повтор {repeat}, "
                    f"время {elapsed:.4f} сек"
                )

            assert outputs["i_j_r"] == outputs["i_r_j"]

            print(f"Повтор {repeat}: результаты совпадают!")

    print("\nИТОГОВЫЕ РЕЗУЛЬТАТЫ")

    averages = {}

    for name, times in results.items():
        times.sort()
        average = mean(times[1:-1])
        averages[name] = average

        print(f"{name}: {average:.4f} сек")

    improvement = averages["i_j_r"] / averages["i_r_j"]

    print(f"\nУскорение нового порядка: {improvement:.2f} раза")


if __name__ == "__main__":
    main()