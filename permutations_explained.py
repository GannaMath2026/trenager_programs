"""
ПРОСТАЯ ВЕРСИЯ ДЛЯ УЧЕНИКА И ДИКТОРА

Что делает программа:
1) Перебирает все варианты соответствия между цифрами 1..7 и буквами A..G.
2) Подставляет буквы вместо цифр в списке дорог из таблицы.
3) Проверяет, что каждая полученная дорога есть в графе
   (или есть та же дорога в обратном порядке).
4) Печатает правильное соответствие.

Как запустить:
python permutations_explained.py
"""

from itertools import permutations
# Берём функцию permutations. Она возвращает все перестановки букв.

# Дороги из таблицы (в виде цифр).
ROADS_FROM_TABLE = '31 41 42 43 51 54 62 64 72 74 75'

# Дороги из графа (в виде букв).
ROADS_FROM_GRAPH = 'AF AG BG BC CG CD DG DE EG EF GF'

for letters_order in permutations('ABCDEFG'):
    # letters_order — один вариант порядка букв.
    # Например: ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    converted_roads = ROADS_FROM_TABLE
    # Сюда будем записывать дороги после замены цифр на буквы.

    for digit, letter in zip('1234567', letters_order):
        # zip создаёт пары:
        # '1' с первой буквой,
        # '2' со второй буквой,
        # и так далее.
        converted_roads = converted_roads.replace(digit, letter)
        # Меняем все вхождения текущей цифры на нужную букву.

    all_roads_match = all(
        road in ROADS_FROM_GRAPH or road[::-1] in ROADS_FROM_GRAPH
        for road in converted_roads.split()
    )
    # split() разбивает строку на отдельные дороги.
    # road in ROADS_FROM_GRAPH — дорога есть в графе.
    # road[::-1] in ROADS_FROM_GRAPH — та же дорога есть в обратном порядке.

    if all_roads_match:
        # Нашли правильное соответствие между цифрами и буквами.
        print('Цифры: ', *'1234567')
        print('Буквы: ', *letters_order)
        print()
