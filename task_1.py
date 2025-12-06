"""
Реалізація хеш-таблиці з розв’язанням колізій через ланцюжки (separate chaining).
Додавання, пошук і видалення елементів здійснюється за ключем.
Клас реалізований в конспекті лекцій. Завдання – додати метод delete.
"""

class HashTable:

    def __init__(self, size: int):
        """
        Ініціалізує хеш-таблицю фіксованого розміру.

        Args:
            size: Кількість бакетів (комірок) у таблиці.
        """
        self.size = size
        # Створюємо список бакетів; кожен бакет — це список пар [key, value].
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key) -> int:
        """
        Обчислює індекс бакета для заданого ключа.

        Args:
            key: ключ будь-якого хешованого типу.

        Returns:
            індекс бакета в межах [0, size-1].
        """
        # Використовуємо modulo size на випадок, якщо hash() поверне від’ємне значення.
        return hash(key) % self.size

    def insert(self, key, value) -> bool:
        """
        Додає або оновлює пару ключ–значення.

        Якщо ключ уже існує в бакеті, значення перезаписується.
        Якщо ключа нема – додається нова пара.

        Args:
            key: ключ.
            value: значення.

        Returns:
            True, якщо вставка/оновлення виконані.
        """
        key_hash = self.hash_function(key)
        key_value = [key, value]  # Пара для вставки.

        # Ініціалізуємо бакет як None
        if self.table[key_hash] is None:
            self.table[key_hash] = [key_value]
            return True
        else:
            # Перевіряємо, чи ключ уже існує і оновлюємо значення.
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True

            # Інакше додаємо нову пару в кінець бакета.
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        """
        Повертає значення за ключем.

        Args:
            key: ключ для пошуку.

        Returns:
            значення, якщо ключ знайдено; інакше None.
        """
        key_hash = self.hash_function(key)

        # Перевіряємо, чи бакет не є None
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]

        return None

    def delete(self, key) -> bool:
        """
        Видаляє пару ключ–значення за заданим ключем.

        Args:
            key: ключ, який треба видалити.

        Returns:
            True, якщо ключ знайдено і видалено; False, якщо ключа не було в таблиці.
        """
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]  # Отримуємо бакет, у якому має бути ключ.

        # Якщо бакет порожній, то нема що видаляти.
        if not bucket:
            return False

        # Шукаємо ключ і видаляємо відповідну пару.
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)  # Видаляємо елемент зі списку бакета.
                return True

        # Ключ не знайдено у бакеті.
        return False


# Приклад використання:
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))   # 10
H.delete("apple")
print(H.get("apple"))   # None

H.delete("orange")
print(H.get("orange"))  # None

print(H.get("banana"))  # 30 (не видалено)
