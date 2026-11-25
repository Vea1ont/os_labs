import time
from multiprocessing import Array, Process, Queue, Value

from lab2.matrix import (
    flatten,
    flatten_checksum,
    generate_matrices,
    generate_triangular_matrices,
    get_range,
    multiply_rows,
    multiply_triangular_matrices,
    multiply_triangular_matrices_dynamic,
)


def worker(A, B, C, m, k, start, end, counter):
    multiply_rows(A, B, C, m, k, start, end, counter)
    
def triangular_worker(A, B, C, n, k, start, end, counter):
    multiply_triangular_matrices(A, B, C, n, k, start, end, counter)
    
def triangular_dynamic_worker(A, B, C, n, k, next_row, counter):
    multiply_triangular_matrices_dynamic(
        A, B, C, n, k, next_row, counter
    )
    
def generator_worker(n, m, k, seed, q):
    A, B = generate_matrices(n, m, k, seed)
    q.put((A, B))
    
def triangular_generator_worker(n, k, seed, q):
    A, B = generate_triangular_matrices(n, k, seed)
    q.put((A, B))
    
def generate_triangular_matrices_separate(n, k, seed):
    q = Queue()
    p = Process(
        target=triangular_generator_worker,
        args= (
            n, k, seed, q
        )
    )
    p.start()
    A, B = q.get()
    p.join()
    q.close()
    
    if p.exitcode != 0:
            raise RuntimeError("Ошибка генерации матриц")
        
    return A, B


def generate_matrices_separate(n, m, k, seed=None):
    q = Queue()
    p = Process(
        target=generator_worker,
        args=(
            n, m, k, seed, q
        )
    )
    p.start()
    A, B = q.get()
    p.join()
    q.close()
    
    if p.exitcode != 0:
        raise RuntimeError("Ошибка генерации матриц")
    
    return A, B
    

def run_multiplication(n, m, k, T, show_progress=False):
    #A, B = generate_matrices(n, m, k, seed=42)
    A, B = generate_matrices_separate(n, m, k, seed=42)
    
    A_shared = Array('q', flatten(A), lock=False)
    B_shared = Array('q', flatten(B), lock=False)
    C_shared = Array('q', n * k, lock=False)

    counter = Value('i', 0)
    processes = []

    for process_id in range(T):
        start, end = get_range(n, T, process_id)

        p = Process(
            target=worker,
            args=(A_shared, B_shared, C_shared,
                  m, k, start, end, counter)
        )
        processes.append(p)

    start_time = time.perf_counter()

    for p in processes:
        p.start()

    if show_progress:
        last_percent = -1

        while any(p.is_alive() for p in processes):
            with counter.get_lock():
                completed = counter.value

            percent = completed * 100 // n

            if percent != last_percent:
                print(f"\rПрогресс: {percent}%", end="", flush=True)
                last_percent = percent

            time.sleep(0.1)

    for p in processes:
        p.join()
        
    failed_processes = [
        p for p in processes
        if p.exitcode != 0
    ]
    
    if failed_processes:
        details = [
            f"PID={p.pid}, код={p.exitcode}"
            for p in failed_processes
        ]
        
        raise RuntimeError(
            f"Некоторые процессы завершились с ошибкой: {details}"
        )

    elapsed = time.perf_counter() - start_time
    checksum = flatten_checksum(C_shared)

    if show_progress:
        print("\rПрогресс: 100%")

    return elapsed, checksum


def run_triangular_multiplication(n, k, T, show_progress=False):
    A, B = generate_triangular_matrices_separate(n, k, seed=42)

    A_shared = Array('q', flatten(A), lock=False)
    B_shared = Array('q', flatten(B), lock=False)
    C_shared = Array('q', n * k, lock=False)

    counter = Value('i', 0)
    processes = []

    for process_id in range(T):
        start, end = get_range(n, T, process_id)

        p = Process(
            target=triangular_worker,
            args=(A_shared, B_shared, C_shared,
                  n, k, start, end, counter)
        )
        processes.append(p)

    start_time = time.perf_counter()

    for p in processes:
        p.start()

    if show_progress:
        last_percent = -1

        while any(p.is_alive() for p in processes):
            with counter.get_lock():
                completed = counter.value

            percent = completed * 100 // n

            if percent != last_percent:
                print(f"\rПрогресс: {percent}%", end="", flush=True)
                last_percent = percent

            time.sleep(0.1)

    for p in processes:
        p.join()

    failed_processes = [
        p for p in processes
        if p.exitcode != 0
    ]

    if failed_processes:
        details = [
            f"PID={p.pid}, код={p.exitcode}"
            for p in failed_processes
        ]
        raise RuntimeError(
            f"Некоторые процессы завершились с ошибкой: {details}"
        )

    elapsed = time.perf_counter() - start_time
    checksum = flatten_checksum(C_shared)

    if show_progress:
        print("\rПрогресс: 100%")

    return elapsed, checksum


def run_triangular_multiplication_dynamic(n, k, T, show_progress=False):
    A, B = generate_triangular_matrices_separate(n, k, seed=42)

    A_shared = Array('q', flatten(A), lock=False)
    B_shared = Array('q', flatten(B), lock=False)
    C_shared = Array('q', n * k, lock=False)

    next_row = Value('i', 0)
    counter = Value('i', 0)

    processes = []

    for _ in range(T):
        p = Process(
            target=triangular_dynamic_worker,
            args=(A_shared, B_shared, C_shared,
                  n, k, next_row, counter)
        )
        processes.append(p)

    start_time = time.perf_counter()

    for p in processes:
        p.start()

    if show_progress:
        last_percent = -1

        while any(p.is_alive() for p in processes):
            with counter.get_lock():
                completed = counter.value

            percent = completed * 100 // n

            if percent != last_percent:
                print(f"\rПрогресс: {percent}%", end="", flush=True)
                last_percent = percent

            time.sleep(0.1)

    for p in processes:
        p.join()

    failed_processes = [
        p for p in processes if p.exitcode != 0
    ]

    if failed_processes:
        raise RuntimeError("Некоторые процессы завершились с ошибкой")

    elapsed = time.perf_counter() - start_time
    checksum = flatten_checksum(C_shared)

    if show_progress:
        print("\rПрогресс: 100%")

    return elapsed, checksum

if __name__ == "__main__":
    for T in [1, 2, 3, 5]:
        elapsed, checksum = run_triangular_multiplication_dynamic(
            n=3,
            k=2,
            T=T,
            show_progress=True
        )

        print(f"T={T}, time={elapsed:.5f}, checksum={checksum}")