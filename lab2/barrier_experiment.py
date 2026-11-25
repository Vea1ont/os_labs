import time
from multiprocessing import Array, Barrier, Process, Value

from lab2.matrix import (
    MOD,
    flatten,
    flatten_checksum,
    generate_matrices,
    get_range,
    matrix_power_sequential,
)


def delayed_worker(A, buf_in, buf_out, n, start, end,
                   steps, barrier, counter, start_delay):
    # задержка имитирует «медленный» процесс (планировщик, нагрузка)
    if start_delay:
        time.sleep(start_delay)

    cur_in = buf_in
    cur_out = buf_out

    for _ in range(steps):
        for i in range(start, end):
            for j in range(n):
                total = 0
                for r in range(n):
                    total = (total + A[i * n + r]
                             * cur_in[r * n + j]) % MOD
                cur_out[i * n + j] = total
            with counter.get_lock():
                counter.value += 1

        if barrier is not None:
            barrier.wait()

        cur_in, cur_out = cur_out, cur_in


def run_demo(n, p, T, use_barrier, delay_pid0):
    A, _ = generate_matrices(n, n, n, seed=42)

    A_shared = Array('q', flatten(A), lock=False)
    buf1 = Array('q', flatten(A), lock=False)
    buf2 = Array('q', n * n, lock=False)

    steps = p - 1
    barrier = Barrier(T) if use_barrier else None
    counter = Value('i', 0)

    processes = []
    for pid in range(T):
        start, end = get_range(n, T, pid)
        processes.append(Process(
            target=delayed_worker,
            args=(A_shared, buf1, buf2, n, start, end,
                  steps, barrier, counter,
                  delay_pid0 if pid == 0 else 0)
        ))

    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()

    current = buf2 if steps % 2 == 1 else buf1
    return flatten_checksum(current)


def main():
    n, p, T = 300, 4, 8

    A, _ = generate_matrices(n, n, n, seed=42)
    ref = sum(sum(row) for row in matrix_power_sequential(A, p))
    print(f"Эталон (последовательно): {ref}")

    for use_barrier in (True, False):
        label = "с барьером" if use_barrier else "без барьера"
        for attempt in range(1, 4):
            got = run_demo(n, p, T, use_barrier, delay_pid0=0.3)
            status = "OK" if got == ref else f"MISMATCH ({got})"
            print(f"{label}, попытка {attempt}: {status}")


if __name__ == "__main__":
    main()
