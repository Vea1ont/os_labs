import time
from multiprocessing import Array, Barrier, Process, Value

from lab2.matrix import flatten, flatten_checksum, get_range
from lab2.parallel import generate_matrices_separate

MOD = 1_000_000_007


def power_worker(A, buf_in, buf_out, n, start, end,
                 steps, barrier, counter):
    cur_in = buf_in
    cur_out = buf_out

    for _ in range(steps):
        # считаем свой блок строк: cur_out = A * cur_in
        for i in range(start, end):
            for j in range(n):
                total = 0
                for r in range(n):
                    total = (total + A[i * n + r]
                             * cur_in[r * n + j]) % MOD
                cur_out[i * n + j] = total
            with counter.get_lock():
                counter.value += 1

        # ждём, пока все процессы закончат шаг
        if barrier is not None:
            barrier.wait()

        # меняем буферы местами: записанный становится исходным
        cur_in, cur_out = cur_out, cur_in


def run_power(n, p, T, show_progress=False, use_barrier=True, seed=42):
    if p < 1:
        raise ValueError("Степень p должна быть >= 1")

    A, _ = generate_matrices_separate(n, n, n, seed=seed)

    A_shared = Array('q', flatten(A), lock=False)
    buf1 = Array('q', flatten(A), lock=False)
    buf2 = Array('q', n * n, lock=False)

    steps = p - 1
    total_rows = steps * n

    barrier = Barrier(T) if use_barrier else None
    counter = Value('i', 0)
    processes = []

    for process_id in range(T):
        start, end = get_range(n, T, process_id)

        proc = Process(
            target=power_worker,
            args=(A_shared, buf1, buf2, n, start, end,
                  steps, barrier, counter)
        )
        processes.append(proc)

    start_time = time.perf_counter()

    for proc in processes:
        proc.start()

    if show_progress and total_rows > 0:
        last_percent = -1

        while any(proc.is_alive() for proc in processes):
            with counter.get_lock():
                completed = counter.value

            percent = completed * 100 // total_rows

            if percent != last_percent:
                print(f"\rПрогресс: {percent}%", end="", flush=True)
                last_percent = percent

            time.sleep(0.1)

    for proc in processes:
        proc.join()

    failed_processes = [
        proc for proc in processes
        if proc.exitcode != 0
    ]

    if failed_processes:
        raise RuntimeError("Некоторые процессы завершились с ошибкой")

    elapsed = time.perf_counter() - start_time

    # после чётного числа шагов результат в buf1, после нечётного — в buf2
    current = buf2 if steps % 2 == 1 else buf1
    checksum = flatten_checksum(current)

    if show_progress and total_rows > 0:
        print("\rПрогресс: 100%")

    return elapsed, checksum
