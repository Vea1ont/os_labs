import random

# Обычные A (n×m) и B (m×k) матрицы
def generate_matrices(n, m, k, seed=None):
    rng = random.Random(seed)
    A = [[rng.randint(0, 9) for _ in range(m)] for _ in range(n)]
    B = [[rng.randint(0, 9) for _ in range(k)] for _ in range(m)]
    return A, B

# Треугольная A
def generate_triangular_matrices(n, k, seed=None):
    rng = random.Random(seed)
    A = [[rng.randint(0, 9) for _ in range(i+1)] for i in range(n)]
    B = [[rng.randint(0, 9) for _ in range(k)] for _ in range(n)]
    return A, B

MOD = 1_000_000_007

# Возведение в степень одним процессом для проверки
def matrix_power_sequential(A, p, mod=MOD):
    n = len(A)
    R = [row[:] for row in A]

    for _ in range(p - 1):
        new_R = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                total = 0
                for r in range(n):
                    total = (total + R[i][r] * A[r][j]) % mod
                new_R[i][j] = total
        R = new_R

    return R


def multiply_matrices(A, B, n, m, k):
    C = [[0 for _ in range(k)] for _ in range(n)]
    
    for i in range(n):
        for j in range(k):
            for r in range(m):
                C[i][j] += A[i][r] * B[r][j]
    
    return C

def multiply_matrices_ikj(A, B, n, m, k):
    C = [[0 for _ in range(k)] for _ in range(n)]

    for i in range(n):
        for r in range(m):
            a = A[i][r]

            for j in range(k):
                C[i][j] += a * B[r][j]

    return C


def multiply_rows(A, B, result, m, k, start, end, counter):
    for i in range(start, end):
        for j in range(k):
            sum_elements = 0
            for r in range(m):
                sum_elements += A[i * m + r] * B[r * k + j]
            result[i * k + j] = sum_elements
        with counter.get_lock():
            counter.value += 1
            
def multiply_triangular_matrices(A, B, result, n, k, start, end, counter):
    for i in range(start, end):
        for j in range(k):
            sum_elements = 0
            for r in range(i + 1):
                a_index = (i * (i + 1)) // 2 + r
                b_index = r * k + j
                sum_elements += A[a_index] * B[b_index]
            result[i * k + j] = sum_elements
        with counter.get_lock():
            counter.value += 1
            
            
            
    

def checksum(C):
    total = 0
    for row in C:
        for value in row:
            total += value
    return total

def flatten(M):
    res = []
    for row in M:
        for value in row:
            res.append(value)  # noqa: PERF402
    return res

def flatten_checksum(C):
    return sum(C)

def get_range(n, T, process_id):
    base = n // T
    remainder = n % T
    start = process_id * base + min(process_id, remainder)
    end = start + base + (1 if process_id < remainder else 0)
    
    return start, end


def multiply_triangular_matrices_dynamic(
    A, B, result, n, k, next_row, counter
):
    while True:
        with next_row.get_lock():
            if next_row.value >= n:
                break
            
            i = next_row.value
            next_row.value += 1
            
        for j in range(k):
            sum_elements = 0
            
            for r in range(i + 1):
                a_index = (i * (i + 1)) // 2 + r
                b_index = r * k + j
                
                sum_elements += A[a_index] * B[b_index]
                
            result[i * k + j] = sum_elements
            
        with counter.get_lock():
            counter.value += 1
