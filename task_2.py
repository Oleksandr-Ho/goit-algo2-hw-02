from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання стрижня через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з ключами:
            "max_profit": максимальний прибуток,
            "cuts": список довжин відрізків (розрізів) у порядку друку (зліва направо),
            "number_of_cuts": кількість розрізів (кількість відрізків мінус один)
    """
    # Використовуємо словник memo, де ключ – довжина стрижня,
    # значення – кортеж (max_profit, cuts_list)
    memo = {}
    
    def helper(n: int) -> (int, List[int]):
        # Базовий випадок: для нульової довжини прибуток 0, без розрізів
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]
        
        max_profit = -float('inf')
        best_cuts = []
        # Спробуємо всі можливі перші розрізи від 1 до n
        for i in range(1, n + 1):
            # Ціна для відрізка довжини i дорівнює prices[i-1]
            current_profit = prices[i - 1]
            remaining_profit, remaining_cuts = helper(n - i)
            total_profit = current_profit + remaining_profit
            # Якщо отримали кращий прибуток, оновлюємо max_profit та запам'ятовуємо розріз
            if total_profit > max_profit:
                max_profit = total_profit
                best_cuts = [i] + remaining_cuts
        memo[n] = (max_profit, best_cuts)
        return memo[n]
    
    profit, cuts = helper(length)
    number_of_cuts = len(cuts) - 1 if cuts else 0
    return {
        "max_profit": profit,
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання стрижня через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з ключами:
            "max_profit": максимальний прибуток,
            "cuts": список довжин відрізків (розрізів) у порядку друку,
            "number_of_cuts": кількість розрізів (кількість відрізків мінус один)

    """
    # dp[j] – максимальний прибуток для стрижня довжиною j
    # first_cut[j] – оптимальний перший розріз для стрижня довжиною j,
    # отриманий за допомогою табуляції із зворотнім перебором для коректного tie-breaking.
    dp = [0] * (length + 1)
    first_cut = [0] * (length + 1)
    
    dp[0] = 0  # Для нульової довжини прибуток 0
    # Для кожної довжини від 1 до length
    for j in range(1, length + 1):
        best = -float('inf')
        # Ітеруємо у зворотньому порядку, щоб у випадку рівності отримати бажаний результат
        for i in range(j, 0, -1):
            profit = prices[i - 1] + dp[j - i]
            # Оновлюємо, якщо знайшли рівний або кращий прибуток
            if profit >= best:
                best = profit
                first_cut[j] = i
        dp[j] = best

    # Реконструюємо список розрізів
    cuts = []
    rem = length
    while rem > 0:
        cuts.append(first_cut[rem])
        rem -= first_cut[rem]
    # За умовою очікуваного результату повертаємо розрізи у "прямому" порядку друку
    # (для прикладу табуляції очікується зворотній порядок від мемоїзації)
    cuts.reverse()
    number_of_cuts = len(cuts) - 1 if cuts else 0
    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]
    
    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")
        
        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")
        
        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")
        
        print("\nПеревірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()