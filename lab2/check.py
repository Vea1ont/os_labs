from lab2.matrix import checksum, get_range, multiply_matrices

A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]
C = multiply_matrices(A, B, 2, 3, 2)

print(C)
print(checksum(C))

A2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
E = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

C2 = multiply_matrices(A2, E, 3, 3, 3)
C3 = multiply_matrices(E, A2, 3, 3, 3)

print(C2 == A2)
print(C3 == A2)

print(C2)
print(checksum(C2))

print(C3)
print(checksum(C3)) 



for process_id in range(5):
    print(process_id, get_range(3, 5, process_id))