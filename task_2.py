"""
Реалізація двійкового пошуку (binary search) для відсортованого масиву з дробовими числами.
"""

from typing import List, Tuple, Optional


def binary_search_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    """
    Повертає (кількість_ітерацій, найменший елемент >= target або None).
    """
    if not arr:                  # Якщо масив порожній, повертаємо 0 і None
        return 0, None

    low, high = 0, len(arr) - 1  # Ініціалізуємо нижню і верхню межі
    iterations = 0               # Ініціалізуємо лічильник ітерацій
    result_index: Optional[int] = None  # Індекс кандидата, який буде повернуто

    while low <= high:           # Поки нижня межа не перевищить верхню
        iterations += 1          # Збільшуємо лічильник ітерацій
        mid = (low + high) // 2  # Обчислюємо середній індекс

        if arr[mid] >= target:       # Якщо елемент середнього індексу >= target
            result_index = mid       # Фіксуємо кандидата як середній індекс
            high = mid - 1           # Опускаємо верхню межу пошуку
        else:
            low = mid + 1            # Піднімаємо нижню межу пошуку

    return iterations, (arr[result_index] if result_index is not None else None)  # Повертаємо кількість ітерацій і значення кандидата


if __name__ == "__main__":
    data = [0.5, 1.2, 3.14, 4.0, 5.5, 7.7]

    iters, upper = binary_search_upper_bound(data, 3.14)
    print("Ітерації:", iters, "Верхня межа:", upper)

    iters, upper = binary_search_upper_bound(data, 4.5)
    print("Ітерації:", iters, "Верхня межа:", upper)

    iters, upper = binary_search_upper_bound(data, -10.0)
    print("Ітерації:", iters, "Верхня межа:", upper)

    iters, upper = binary_search_upper_bound(data, 100.0)
    print("Ітерації:", iters, "Верхня межа:", upper)
