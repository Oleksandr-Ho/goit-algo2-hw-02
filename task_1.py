from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str         # Унікальний ідентифікатор завдання
    volume: float   # Об'єм моделі (в см³)
    priority: int   # Пріоритет завдання (1 – найвищий, 3 – найнижчий)
    print_time: int # Час друку в хвилинах

@dataclass
class PrinterConstraints:
    max_volume: float  # Максимальний сумарний об'єм моделі для одночасного друку
    max_items: int     # Максимальна кількість моделей для одночасного друку

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера.

    Args:
        print_jobs: Список завдань на друк. Кожне завдання містить ключі:
                    "id", "volume", "priority", "print_time".
        constraints: Обмеження принтера у вигляді словника з ключами:
                    "max_volume" та "max_items".

    Алгоритм:
      1. Перетворення вхідних даних у об'єкти PrintJob та PrinterConstraints.
      2. Сортування завдань за пріоритетом (нижче значення – вищий пріоритет).
      3. Групування завдань для одночасного друку:
         - До однієї групи можна додати завдання, якщо:
              * Загальна кількість завдань у групі не перевищує max_items.
              * Сумарний об'єм завдань не перевищує max_volume.
         - Час друку групи визначається як максимальний час серед завдань цієї групи.
      4. Загальний час друку – сума часів друку усіх груп.
      5. Повернення словника з оптимальним порядком друку (список ID завдань)
         та загальним часом друку.

    Returns:
        Dict з ключами:
            "print_order": список ідентифікаторів завдань у порядку друку,
            "total_time": загальний час друку (в хвилинах)
    """
    # Перетворення вхідних даних у об'єкти
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Сортування завдань за пріоритетом (за зростанням; 1 – найвищий)
    jobs.sort(key=lambda job: job.priority)

    optimal_order = []   # Список для зберігання порядку друку (ID завдань)
    total_time = 0       # Загальний час друку

    # Ініціалізація поточної групи друку
    current_group = []       # Завдання, що друкуються одночасно
    current_group_volume = 0 # Сумарний об'єм завдань у групі
    current_group_time = 0   # Максимальний час друку серед завдань групи

    # Проходимо по всіх завданнях
    for job in jobs:
        # Перевіряємо, чи можна додати завдання до поточної групи
        if (len(current_group) < printer.max_items and 
            current_group_volume + job.volume <= printer.max_volume):
            # Додаємо завдання до групи
            current_group.append(job)
            current_group_volume += job.volume
            current_group_time = max(current_group_time, job.print_time)
        else:
            # Завершуємо поточну групу, якщо додавання нового завдання
            # порушує обмеження принтера
            if current_group:
                # Додаємо ідентифікатори завдань з поточної групи до загального порядку
                optimal_order.extend([j.id for j in current_group])
                # Додаємо час друку групи до загального часу
                total_time += current_group_time
            # Починаємо нову групу з поточним завданням
            current_group = [job]
            current_group_volume = job.volume
            current_group_time = job.print_time

    # Обробка залишку завдань (якщо остання група не пуста)
    if current_group:
        optimal_order.extend([j.id for j in current_group])
        total_time += current_group_time

    return {
        "print_order": optimal_order,
        "total_time": total_time
    }

# Тестування оптимізації черги 3D-друку
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна робота
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна робота
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,  # максимальний сумарний об'єм моделі для друку
        "max_items": 2      # максимальна кількість моделей одночасно
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")
    # Очікуваний результат:
    # Порядок друку: ['M1', 'M2', 'M3']
    # Загальний час: 270 хвилин

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")
    # Очікуваний результат:
    # Порядок друку: ['M2', 'M1', 'M3']
    # Загальний час: 270 хвилин

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")
    # Очікуваний результат:
    # Порядок друку: ['M1', 'M2', 'M3']
    # Загальний час: 450 хвилин

if __name__ == "__main__":
    test_printing_optimization()
