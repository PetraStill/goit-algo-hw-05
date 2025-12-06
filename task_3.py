"""
Модуль для порівняння ефективності алгоритмів пошуку підрядка
в текстових файлах.

Реалізовані алгоритми пошуку:
- Алгоритм Боєра–Мура (Boyer–Moore) з евристикою "поганого символу";
- Алгоритм Кнута–Морріса–Пратта (Knuth–Morris–Pratt, KMP);
- Алгоритм Рабіна–Карпа (Rabin–Karp) на основі хеш-функції.

Сценарій роботи модуля:
1. Зчитування вмісту двох текстових файлів (стаття 1, стаття 2).
2. Визначення двох видів підрядків для кожного тексту:
   - підрядок, який існує в тексті;
   - підрядок, якого немає в тексті.
3. Вимірювання часу виконання кожного алгоритму за допомогою timeit
   для кожного з підрядків.
4. Порівняння швидкодії алгоритмів окремо для кожного тексту
   та загалом.
5. Формування звіту у форматі Markdown з таблицями результатів та
   текстовими висновками, запис у файл `substring_search_results.md`.
"""

from __future__ import annotations

import timeit
from typing import Callable, Dict, List


def boyer_moore_search(text: str, pattern: str) -> int:
    """
    Виконує пошук підрядка в рядку за алгоритмом Боєра–Мура
    з використанням евристики "поганого символу".

    Параметри:
        text (str): текст, у якому виконується пошук;
        pattern (str): підрядок, який шукаємо.

    Повертає:
        int: індекс першого входження підрядка у тексті
             або -1, якщо підрядок не знайдено.
    """
    n = len(text)
    m = len(pattern)

    # Перевіряємо крайові випадки та одразу повертаємо результат
    if m == 0:
        return 0
    if m > n:
        return -1

    # Створюємо таблицю зсувів "поганого символу" для шаблону
    bad_char_shift: Dict[str, int] = {}
    for i in range(m - 1):
        bad_char_shift[pattern[i]] = m - 1 - i

    # Запускаємо вирівнювання шаблону по тексту
    index = 0
    while index <= n - m:
        # Порівнюємо символи справа наліво
        j = m - 1
        while j >= 0 and text[index + j] == pattern[j]:
            j -= 1

        # Фіксуємо знаходження повного збігу
        if j < 0:
            return index

        # Обчислюємо зсув за невідповідним символом та зсуваємо шаблон
        bad_char = text[index + j]
        shift = bad_char_shift.get(bad_char, m)
        index += max(1, shift)

    # Повертаємо -1, якщо підрядок не знайдено
    return -1


def kmp_prefix_function(pattern: str) -> List[int]:
    """
    Обчислює масив префікс-функції (LPS – longest proper prefix which is also suffix)
    для алгоритму Кнута–Морріса–Пратта.

    Параметри:
        pattern (str): підрядок, для якого будується префікс-функція.

    Повертає:
        List[int]: список значень префікс-функції для кожної позиції шаблону.
    """
    m = len(pattern)
    lps = [0] * m

    # Формуємо значення LPS, рухаючись зліва направо
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text: str, pattern: str) -> int:
    """
    Виконує пошук підрядка в рядку за алгоритмом Кнута–Морріса–Пратта.

    Параметри:
        text (str): текст, у якому виконується пошук;
        pattern (str): підрядок, який шукаємо.

    Повертає:
        int: індекс першого входження підрядка у тексті
             або -1, якщо підрядок не знайдено.
    """
    n = len(text)
    m = len(pattern)

    # Перевіряємо крайові випадки та одразу повертаємо результат
    if m == 0:
        return 0
    if m > n:
        return -1

    # Будуємо LPS для шаблону
    lps = kmp_prefix_function(pattern)

    # Запускаємо посимвольний пошук з використанням LPS
    i = 0
    j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

    # Повертаємо -1, якщо підрядок не знайдено
    return -1


def rabin_karp_search(text: str, pattern: str, base: int = 256, mod: int = 10**9 + 7) -> int:
    """
    Виконує пошук підрядка в рядку за алгоритмом Рабіна–Карпа
    з використанням ролінгового хешу.

    Параметри:
        text (str): текст, у якому виконується пошук;
        pattern (str): підрядок, який шукаємо;
        base (int): основа для обчислення хешу (кількість можливих символів);
        mod (int): модуль для зменшення значень хешу.

    Повертає:
        int: індекс першого входження підрядка у тексті
             або -1, якщо підрядок не знайдено.
    """
    n = len(text)
    m = len(pattern)

    # Перевіряємо крайові випадки та одразу повертаємо результат
    if m == 0:
        return 0
    if m > n:
        return -1

    # Готуємо степінь base для ролінгового хешу
    highest_power = pow(base, m - 1, mod)

    # Обчислюємо стартові хеші для шаблону та першого вікна тексту
    hash_pattern = 0
    hash_text = 0
    for i in range(m):
        hash_pattern = (hash_pattern * base + ord(pattern[i])) % mod
        hash_text = (hash_text * base + ord(text[i])) % mod

    # Перевіряємо перше вікно
    if hash_pattern == hash_text and text[:m] == pattern:
        return 0

    # Рухаємо вікно по тексту та оновлюємо хеш
    for i in range(m, n):
        hash_text = (hash_text - ord(text[i - m]) * highest_power) % mod
        hash_text = (hash_text * base + ord(text[i])) % mod
        hash_text = (hash_text + mod) % mod

        # Перевіряємо реальний збіг при рівності хешів
        if hash_text == hash_pattern:
            start = i - m + 1
            if text[start:start + m] == pattern:
                return start

    # Повертаємо -1, якщо підрядок не знайдено
    return -1


def measure_time(
    func: Callable[[str, str], int],
    text: str,
    pattern: str,
    repetitions: int = 100
) -> float:
    """
    Вимірює час виконання функції пошуку підрядка за допомогою timeit.

    Параметри:
        func: функція пошуку (Boyer–Moore, KMP, Rabin–Karp тощо);
        text (str): текст, у якому виконується пошук;
        pattern (str): підрядок, який шукаємо;
        repetitions (int): кількість повторів виклику функції
                           для усереднення часу.

    Повертає:
        float: сумарний час виконання всіх повторів (у секундах).
    """
    # Створюємо таймер та виконуємо потрібну кількість повторів
    timer = timeit.Timer(lambda: func(text, pattern))
    return timer.timeit(number=repetitions)


def generate_markdown_report(
    results: List[Dict[str, object]],
    best_per_text: Dict[str, str],
    best_overall: str,
    repetitions: int
) -> str:
    """
    Формує Markdown-звіт за результатами вимірювань.

    Параметри:
        results: список словників з полями:
                 - text_name: назва тексту;
                 - pattern_type: тип підрядка ("existing"/"missing");
                 - algorithm: назва алгоритму;
                 - time: виміряний сумарний час;
        best_per_text: словник {назва_тексту: найшвидший_алгоритм};
        best_overall: назва найшвидшого алгоритму загалом;
        repetitions: кількість повторів, використаних у вимірюваннях.

    Повертає:
        str: рядок із вмістом файлу у форматі Markdown.
    """
    # Формуємо заголовки та таблицю результатів
    lines: List[str] = [
        "# Порівняння алгоритмів пошуку підрядка\n",
        f"Кількість повторів для кожного вимірювання: **{repetitions}**.\n",
        "## Результати вимірювань\n",
        "| Текст | Тип підрядка | Алгоритм | Час, с (сумарно) |",
        "|-------|--------------|----------|------------------|",
    ]

    for r in results:
        lines.append(
            f"| {r['text_name']} | {r['pattern_type']} | {r['algorithm']} | {r['time']:.6f} |"
        )

    # Додаємо підсумки по кожному тексту та загалом
    lines.append("\n## Найшвидший алгоритм для кожного тексту\n")
    for text_name, algo in best_per_text.items():
        lines.append(f"- **{text_name}**: найшвидший алгоритм – **{algo}**")

    lines.append("\n## Найшвидший алгоритм загалом\n")
    lines.append(
        "З урахуванням усіх вимірювань по обох текстах та обох типах підрядків "
        f"найменший сумарний час показав алгоритм **{best_overall}**.\n"
    )

    lines.append("## Коментарі\n")
    lines.append(
        "- Порівняння виконувалося на конкретних текстах (дві статті) "
        "та вибраних підрядках; на інших даних відносні результати можуть відрізнятися.\n"
    )

    return "\n".join(lines)


if __name__ == "__main__":
    # Задаємо імена файлів зі статтями
    file1 = "стаття 1.txt"
    file2 = "стаття 2.txt"

    # Зчитуємо тексти зі файлів
    with open(file1, "r", encoding="utf-8") as f:
        text1 = f.read()
    with open(file2, "r", encoding="utf-8") as f:
        text2 = f.read()

    # Обираємо підрядки для першого та другого тексту
    existing_pattern_1 = "жадібний алгоритм"
    missing_pattern_1 = "квантовий дракон"
    existing_pattern_2 = "рекомендаційної системи"
    missing_pattern_2 = "суперпозиція котиків"

    # Формуємо словник алгоритмів для перебору
    algorithms: Dict[str, Callable[[str, str], int]] = {
        "Boyer-Moore": boyer_moore_search,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp_search,
    }

    # Запускаємо вимірювання часу для кожного алгоритму
    repetitions = 100
    results: List[Dict[str, object]] = []

    for pattern, pattern_type in [
        (existing_pattern_1, "existing"),
        (missing_pattern_1, "missing"),
    ]:
        for algo_name, algo_func in algorithms.items():
            t = measure_time(algo_func, text1, pattern, repetitions=repetitions)
            results.append(
                {
                    "text_name": "стаття 1",
                    "pattern_type": pattern_type,
                    "algorithm": algo_name,
                    "time": t,
                }
            )

    for pattern, pattern_type in [
        (existing_pattern_2, "existing"),
        (missing_pattern_2, "missing"),
    ]:
        for algo_name, algo_func in algorithms.items():
            t = measure_time(algo_func, text2, pattern, repetitions=repetitions)
            results.append(
                {
                    "text_name": "стаття 2",
                    "pattern_type": pattern_type,
                    "algorithm": algo_name,
                    "time": t,
                }
            )

    # Визначаємо найшвидший алгоритм для кожного тексту
    best_per_text: Dict[str, str] = {}
    for text_name in ["стаття 1", "стаття 2"]:
        sums: Dict[str, float] = {name: 0.0 for name in algorithms.keys()}
        for r in results:
            if r["text_name"] == text_name:
                sums[r["algorithm"]] += float(r["time"])
        best_per_text[text_name] = min(sums.items(), key=lambda x: x[1])[0]

    # Визначаємо найшвидший алгоритм загалом
    overall_sums: Dict[str, float] = {name: 0.0 for name in algorithms.keys()}
    for r in results:
        overall_sums[r["algorithm"]] += float(r["time"])
    best_overall = min(overall_sums.items(), key=lambda x: x[1])[0]

    # Генеруємо та записуємо Markdown-звіт
    markdown_report = generate_markdown_report(
        results=results,
        best_per_text=best_per_text,
        best_overall=best_overall,
        repetitions=repetitions,
    )
    with open("substring_search_results.md", "w", encoding="utf-8") as md_file:
        md_file.write(markdown_report)

    # Виводимо коротке резюме у консоль
    print("Найшвидший алгоритм для кожного тексту:")
    for text_name, algo in best_per_text.items():
        print(f"- {text_name}: {algo}")

    print(f"\nНайшвидший алгоритм загалом: {best_overall}")
    print('Детальні результати збережено у файлі "substring_search_results.md".')
