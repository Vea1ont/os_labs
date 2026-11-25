import unittest

from lab2.matrix import (
    checksum,
    generate_matrices,
    generate_triangular_matrices,
    matrix_power_sequential,
    multiply_matrices,
)
from lab2.parallel import (
    generate_matrices_separate,
    run_multiplication,
    run_triangular_multiplication,
    run_triangular_multiplication_dynamic,
)
from lab2.power import run_power


class TestSequentialMultiplication(unittest.TestCase):
    def test_known_result_2x2(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        self.assertEqual(
            multiply_matrices(A, B, 2, 2, 2),
            [[19, 22], [43, 50]],
        )

    def test_known_result_2x3_by_3x2(self):
        A = [[1, 2, 3], [4, 5, 6]]
        B = [[7, 8], [9, 10], [11, 12]]
        self.assertEqual(
            multiply_matrices(A, B, 2, 3, 2),
            [[58, 64], [139, 154]],
        )

    def test_identity(self):
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        E = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertEqual(multiply_matrices(A, E, 3, 3, 3), A)
        self.assertEqual(multiply_matrices(E, A, 3, 3, 3), A)

    def test_zero_matrix(self):
        A = [[1, 2], [3, 4]]
        Z = [[0, 0], [0, 0]]
        self.assertEqual(
            multiply_matrices(A, Z, 2, 2, 2), [[0, 0], [0, 0]]
        )

    def test_edge_shapes(self):
        self.assertEqual(multiply_matrices([[5]], [[3]], 1, 1, 1),
                         [[15]])
        self.assertEqual(
            multiply_matrices([[1, 2, 3]], [[1], [2], [3]], 1, 3, 1),
            [[14]],
        )
        self.assertEqual(
            multiply_matrices([[1], [2], [3]], [[1, 2, 3]], 3, 1, 3),
            [[1, 2, 3], [2, 4, 6], [3, 6, 9]],
        )


class TestParallelMultiplication(unittest.TestCase):
    def test_parallel_matches_sequential(self):
        n, m, k = 12, 10, 8
        A, B = generate_matrices(n, m, k, seed=42)
        expected = checksum(multiply_matrices(A, B, n, m, k))

        for T in (1, 2, 3, 7, 16):
            with self.subTest(T=T):
                _, got = run_multiplication(n, m, k, T)
                self.assertEqual(got, expected)

    def test_ipc_generation_matches_local(self):
        local = generate_matrices(10, 8, 6, seed=42)
        via_ipc = generate_matrices_separate(10, 8, 6, seed=42)
        self.assertEqual(local, via_ipc)


class TestTriangular(unittest.TestCase):
    def test_static_matches_dynamic(self):
        n, k = 40, 25
        for T in (1, 2, 3, 7, 50):
            with self.subTest(T=T):
                _, static_sum = run_triangular_multiplication(
                    n, k, T
                )
                _, dynamic_sum = (
                    run_triangular_multiplication_dynamic(n, k, T)
                )
                self.assertEqual(static_sum, dynamic_sum)

    def test_triangular_row_lengths(self):
        A, B = generate_triangular_matrices(4, 3, seed=1)
        self.assertEqual([len(row) for row in A], [1, 2, 3, 4])
        self.assertEqual([len(row) for row in B], [3, 3, 3, 3])


class TestPower(unittest.TestCase):
    def test_power_one_is_identity_operation(self):
        n = 8
        A, _ = generate_matrices(n, n, n, seed=42)
        _, got = run_power(n, 1, 4)
        self.assertEqual(got, checksum(A))

    def test_identity_matrix_power(self):
        n = 6
        E = [[1 if i == j else 0 for j in range(n)]
             for i in range(n)]
        self.assertEqual(matrix_power_sequential(E, 6), E)

    def test_parallel_power_matches_sequential(self):
        n, p = 10, 4
        A, _ = generate_matrices(n, n, n, seed=42)
        expected = checksum(matrix_power_sequential(A, p))

        for T in (1, 2, 3, 7, 14):
            with self.subTest(T=T):
                _, got = run_power(n, p, T)
                self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
