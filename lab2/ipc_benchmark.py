import csv
import os
import time
from multiprocessing import Process, Queue

from lab2.matrix import generate_triangular_matrices

SIZES = [300, 500, 750]
REPEATS = 5
OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "result", "grade4", "ipc_transfer.csv",
)


def timed_generator(n, k, seed, q):
    start = time.perf_counter()
    A, B = generate_triangular_matrices(n, k, seed)
    gen_time = time.perf_counter() - start
    q.put((A, B, gen_time))


def main():
    with open(OUTPUT, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "matrix_size", "repeat",
            "generation_seconds", "total_seconds",
            "transfer_seconds",
        ])

        for size in SIZES:
            for repeat in range(1, REPEATS + 1):
                q = Queue()
                p = Process(
                    target=timed_generator,
                    args=(size, size, 42, q),
                )

                start = time.perf_counter()
                p.start()
                A, B, gen_time = q.get()
                total = time.perf_counter() - start
                p.join()
                q.close()

                transfer = total - gen_time
                writer.writerow([
                    size, repeat,
                    gen_time, total, transfer,
                ])
                file.flush()
                print(
                    f"Size: {size} | Repeat: {repeat} | "
                    f"gen: {gen_time:.4f}s | "
                    f"transfer: {transfer:.4f}s",
                    flush=True,
                )


if __name__ == "__main__":
    main()
