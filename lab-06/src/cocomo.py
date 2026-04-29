from dataclasses import dataclass
from math import prod, ceil


@dataclass
class Driver:
    nominal = 1 # Номинальное значение драйвера
    #high_modp = 0.91
    #high_tool = 0.91

# Словарь FACTORS: коэффициенты формул COCOMO для трёх режимов проекта
FACTORS = {
    'C1': [3.20, 3.00, 2.80], # Множитель трудоёмкости для режимов
    'P1': [1.05, 1.12, 1.20], # Показатель степени для трудоёмкости
 
    'C2': [2.50, 2.50, 2.50], # Множитель времени разработки
    'P2': [0.38, 0.35, 0.32]  # Показатель степени для времени
}

# Словарь DRIVERS: возможные числовые значения множителей для каждого фактора
DRIVERS = {
    'RELY': [0.75, 0.86, 1.00, 1.15, 1.40], # Надёжность (5 уровней)
    'DATA': [0.94, 1.00, 1.08, 1.16],       # Размер БД (4 уровня)
    'CPLX': [0.70, 0.85, 1.00, 1.15, 1.30], # Сложность продукта (5 уровней)

    'TIME': [1.00, 1.11, 1.50],             # Ограничение времени выполнения (3 уровня)
    'STOR': [1.00, 1.06, 1.21],             # Ограничение памяти (3 уровня)
    'VIRT': [0.87, 1.00, 1.15, 1.30],       # Изменчивость виртуальной машины (4 уровня)
    'TURN': [0.87, 1.00, 1.07, 1.15],       # Время реакции (4 уровня)

    'ACAP': [1.46, 1.19, 1.00, 0.86, 0.71], # Способности аналитика (5 уровней)
    'AEXP': [1.29, 1.15, 1.00, 0.91, 0.82], # Знание приложений (5 уровней)
    'PCAP': [1.42, 1.17, 1.00, 0.86, 0.70], # Способности программиста (5 уровней)
    'VEXP': [1.21, 1.10, 1.00, 0.90],       # Знание виртуальной машины (4 уровня)
    'LEXP': [1.14, 1.07, 1.00, 0.95],       # Знание языка (4 уровня)

    'MODP': [1.24, 1.10, 1.00, 0.91, 0.82], # Использование методов (5 уровней)
    'TOOL': [1.24, 1.10, 1.00, 0.91, 0.82], # Использование инструментов (5 уровней)
    'SCED': [1.23, 1.08, 1.00, 1.04, 1.10]  # Сроки разработки (5 уровней)
}

# DRIVERS_INDEXES: закрепляет каждый драйвер за индексом в списке из 15 элементов
DRIVERS_INDEXES = {
    'RELY': 0,
    'DATA': 1,
    'CPLX': 2,

    'TIME': 3,
    'STOR': 4,
    'VIRT': 5,
    'TURN': 6,

    'ACAP': 7,
    'AEXP': 8,
    'PCAP': 9,
    'VEXP': 10,
    'LEXP': 11,

    'MODP': 12,
    'TOOL': 13,
    'SCED': 14
}


# Функция оценки трудоёмкости (work) и времени (time) разработки
def evaluate_project(mode_index: int, drivers: list, kloc: float):
    # Получаем коэффициент C1 для выбранного режима
    c1 = FACTORS['C1'][mode_index]
    # Получаем показатель степени P1 для выбранного режима
    p1 = FACTORS['P1'][mode_index]
    # Вычисляем множитель корректировки EAF как произведение всех 15 драйверов
    eaf = prod(drivers)
    # Формула трудоёмкости: C1 * EAF * (KLOC ^ P1)
    work = c1 * eaf * kloc ** p1
    # Получаем коэффициент C2 для выбранного режима
    c2 = FACTORS['C2'][mode_index]
    # Получаем показатель степени P2 для выбранного режима
    p2 = FACTORS['P2'][mode_index]
    # Формула времени разработки: C2 * (трудоёмкость ^ P2)
    time = c2 * work ** p2

    return work, time

# Функция распределения трудоёмкости и времени по стадиям жизненного цикла
def get_life_cycle(work: float, time: float):
    return {
        0: {'time%':  36, 'time': time * 0.36, 'work%':   8, 'work': work * 0.08, 'employees': ceil((work * 0.08) / (time * 0.36))},
        1: {'time%':  36, 'time': time * 0.36, 'work%':  18, 'work': work * 0.18, 'employees': ceil((work * 0.18) / (time * 0.36))},
        2: {'time%':  18, 'time': time * 0.18, 'work%':  25, 'work': work * 0.25, 'employees': ceil((work * 0.25) / (time * 0.18))},
        3: {'time%':  18, 'time': time * 0.18, 'work%':  26, 'work': work * 0.26, 'employees': ceil((work * 0.26) / (time * 0.18))},
        4: {'time%':  28, 'time': time * 0.28, 'work%':  31, 'work': work * 0.31, 'employees': ceil((work * 0.31) / (time * 0.28))},
        5: {'time%': 100, 'time': time * 1.00, 'work%': 100, 'work': work * 1.00, 'employees': ceil((work * 1.00) / (time * 1.00))},
        6: {'time%': 136, 'time': time * 1.36, 'work%': 108, 'work': work * 1.08, 'employees': ceil((work * 1.08) / (time * 1.36))},
    }

# Функция распределения трудозатрат по видам деятельности (WBS) с учётом зарплаты
def get_wbs(work: float, salary: float):
    return {
        0: {'budget%':   4, 'work': work * 0.04, 'costs': (work * 0.04) * salary},
        1: {'budget%':  12, 'work': work * 0.12, 'costs': (work * 0.12) * salary},
        2: {'budget%':  44, 'work': work * 0.44, 'costs': (work * 0.44) * salary},
        3: {'budget%':   6, 'work': work * 0.06, 'costs': (work * 0.06) * salary},
        4: {'budget%':  14, 'work': work * 0.14, 'costs': (work * 0.14) * salary},
        5: {'budget%':   7, 'work': work * 0.07, 'costs': (work * 0.07) * salary},
        6: {'budget%':   7, 'work': work * 0.07, 'costs': (work * 0.07) * salary},
        7: {'budget%':   6, 'work': work * 0.06, 'costs': (work * 0.06) * salary},
        8: {'budget%': 100, 'work': work * 1.00, 'costs': (work * 1.00) * salary},
    }