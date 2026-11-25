from lab2.parallel import run_multiplication

    
def main():
    values = input("Введите n m k T: ").split()

    if len(values) != 4:
        raise ValueError("Нужно ввести ровно 4 числа: n m k T")

    try:
        n, m, k, T = map(int, values)
    except ValueError:
        raise ValueError("Все параметры должны быть целыми числами")

    if min(n, m, k, T) <= 0:
        raise ValueError("Все параметры должны быть положительными")

    elapsed, checksum = run_multiplication(
        n, m, k, T, show_progress=True
    )

    print(f"Время: {elapsed:.4f} сек")
    print(f"Контрольная сумма: {checksum}")

        
if __name__ == "__main__":
    main()