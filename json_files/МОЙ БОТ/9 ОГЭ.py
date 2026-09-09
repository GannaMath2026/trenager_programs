from itertools import permutations

# --- ИСХОДНЫЕ ДАННЫЕ ---
vertices = '1234'
edges_digit = '12 13 14 23 34'
edges_letter = 'BA AD AC CB DC'  # эталон
letters = 'ABCD'

# Преобразуем эталон в множество для сравнения
target_set = set(''.join(sorted(e)) for e in edges_letter.split())

print("🔹 ИСХОДНЫЕ ДАННЫЕ")
print(f"   Цифровой граф (рёбра): {edges_digit}")
print(f"   Буквенный граф (эталон): {edges_letter}")
print()
print("=" * 70)
print("ПЕРЕБОР ВСЕХ ПЕРЕСТАНОВОК")
print("=" * 70)

for perm in permutations(letters):
    mapping = {v: perm[i] for i, v in enumerate(vertices)}

    # Заменяем цифры на буквы
    edges_new = edges_digit
    for digit, letter in mapping.items():
        edges_new = edges_new.replace(digit, letter)

    # Преобразуем в множество для сравнения
    new_set = set(''.join(sorted(e)) for e in edges_new.split())
    valid = (new_set == target_set)

    # Вывод в новом формате
    print(f"\n📌 Перестановка: {''.join(perm)}")
    print(f"   Было (цифровой): {edges_digit}")
    print(f"   Стало (после замены): {edges_new}")
    print(f"   Сравниваем с эталоном: {edges_letter}")
    print(f"   Результат: {'✅ ПОДХОДИТ' if valid else '❌ НЕ ПОДХОДИТ'}")