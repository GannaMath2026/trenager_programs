import json
import os

# 1. Собираем задачи
tasks = []
files = ['informatika25_делители.json', 'informatika25_маски.json', 'informatika25_простые_множители.json']

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            section = filename.replace('informatika25_', '').replace('.json', '').capitalize()
            for item in data:
                difficulty = "Сложный" if any(
                    x in item.get("name", "").lower() for x in ["сложный", "секунд", "product"]) else "Базовый"

                code_no = item.get("codeNoComments", "").strip()
                code_with = item.get("codeWithComments", "").strip()
                if not code_no: code_no = code_with
                if not code_with: code_with = code_no

                codes = {
                    "Без комментариев": code_no,
                    "С комментариями": code_with,
                    "Рекурсия — без комментариев": code_no,
                    "Рекурсия — с комментариями": code_with
                }

                tasks.append({
                    "id": item.get("name", "Без названия"),
                    "title": item.get("name", ""),
                    "desc": item.get("text", ""),
                    "question": "",
                    "answer": item.get("answer", ""),
                    "section": section,
                    "difficulty": difficulty,
                    "codes": codes,
                    "methods": ["Без комментариев", "С комментариями", "Рекурсия — без комментариев",
                                "Рекурсия — с комментариями"]
                })


def sort_key(t):
    diff_score = 1 if t["difficulty"] == "Сложный" else 2
    return (t["section"], diff_score, t["title"])


tasks.sort(key=sort_key)

print(f"✅ Загружено задач: {len(tasks)}")

# 2. Читаем исходный файл
if not os.path.exists('source_19.html'):
    print("❌ ОШИБКА: файл 'source_19.html' не найден в текущей папке!")
    print(
        "Пожалуйста, положите ваш рабочий файл '19_last_28-10.html' в эту папку и переименуйте его в 'source_19.html'.")
    exit(1)

with open('source_19.html', 'r', encoding='utf-8') as f:
    html = f.read()
print("✅ Исходный файл прочитан.")

# 3. Замена TASKS
start_idx = html.find("const TASKS=")
if start_idx == -1:
    start_idx = html.find("const TASKS =")
if start_idx == -1:
    print("❌ ОШИБКА: в файле source_19.html не найдена строка 'const TASKS='")
    exit(1)

end_marker = "let conditionFont="
end_idx = html.find(end_marker, start_idx)
if end_idx == -1:
    print("❌ ОШИБКА: не найдена строка 'let conditionFont=' после массива задач")
    exit(1)

new_tasks_js = json.dumps(tasks, ensure_ascii=False)
html = html[:start_idx] + "const TASKS= " + new_tasks_js + ";\n" + html[end_idx:]
print("✅ Массив задач заменён.")

# 4. Замена INITIAL_USER_STATE
state_start_idx = html.find("const INITIAL_USER_STATE=")
if state_start_idx != -1:
    state_end_marker = "const DEFAULT_USER_STATE="
    state_end_idx = html.find(state_end_marker, state_start_idx)
    if state_end_idx != -1:
        default_state = {
            "students": [{"id": "s1", "name": "Ученик 1"}],
            "current": "s1",
            "filtersByStudent": {"s1": {"q": "", "done": None, "fav": None, "dz": None}},
            "sectionByStudent": {"s1": None},
            "progressByStudent": {"s1": {}}
        }
        html = html[:state_start_idx] + "const INITIAL_USER_STATE=" + json.dumps(default_state,
                                                                                 ensure_ascii=False) + ";\n" + html[
                                                                                                               state_end_idx:]
        print("✅ Прогресс сброшен.")

# 5. Сохранение и вывод пути
output_file = os.path.abspath('app_ready.html')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "=" * 50)
print(f"🎉 ГОТОВО! Файл сохранён по пути:")
print(f"👉 {output_file}")
print("=" * 50)
print("\nСкопируйте этот путь, откройте проводник и запустите файл app_ready.html")