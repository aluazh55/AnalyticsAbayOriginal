import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Настройка сценариев
scenarios = {
    "NoAlgo": "metrics_NoAlgo.csv",
    "Gridlock": "metrics_mpc_Gridlock.csv",
    "OffsetSplit": "metrics_OffsetSplit.csv",
    "OffsetOnly": "metrics_OffsetOnly.csv"
}

# Красивые русские названия для легенды
scenarios_ru = {
    "NoAlgo": "Без алгоритма",
    "Gridlock": "Gridlock (MPC)",
    "OffsetSplit": "Offset + Split",
    "OffsetOnly": "Только Offset"
}

# Загрузка и сглаживание данных (каждые 20 строк объединяются в среднее)
dfs = {}
for name, path in scenarios.items():
    if os.path.exists(path):
        df_raw = pd.read_csv(path)
        # Группируем по 20 строк и берем среднее значение для сглаживания графиков
        df_smoothed = df_raw.groupby(df_raw.index // 20).mean()
        dfs[scenarios_ru[name]] = df_smoothed

# 2. Построение графиков сравнения во времени (сглаженные данные)
PLOTS = [
    ("travel_time", "Время (с)", "Среднее время в пути"),
    ("queue", "Кол-во ТС", "Длина очередей"),
    ("throughput", "Транспортных средств/мин", "Пропускная способность"),
    ("speed", "м/с", "Средняя скорость"),
    ("spillback", "Кол-во событий", "Инциденты заторов (Spillback)"),
    ("co2_rate_mg", "мг/мин", "Выбросы CO2"),
]

fig, axes = plt.subplots(3, 2, figsize=(16, 15))
fig.suptitle("Анализ эффективности алгоритмов управления (сглаженные данные)", fontsize=18)

for ax, (col, ylabel, title) in zip(axes.flat, PLOTS):
    for name, df in dfs.items():
        # Используем сглаженное время по оси X и сглаженный параметр по оси Y
        ax.plot(df["time"], df[col], label=name, alpha=0.9, linewidth=2)
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("Время симуляции (с)", fontsize=10)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(fontsize=9)

plt.subplots_adjust(hspace=0.4, wspace=0.3, top=0.92)
plt.savefig("zcombineplots31.png", dpi=200, bbox_inches='tight')

# 3. Статистический анализ (Box Plots на основе сглаженных данных для оценки стабильности)
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))

# Сравнение скоростей
speed_data = pd.DataFrame({name: df["speed"] for name, df in dfs.items()})
sns.boxplot(data=speed_data, ax=axes2[0])
axes2[0].set_title("Распределение скоростей")
axes2[0].set_ylabel("м/с")
# ИСПРАВЛЕНО: Безопасный поворот подписей
axes2[0].tick_params(axis='x', rotation=15)

# Сравнение очередей
queue_data = pd.DataFrame({name: df["queue"] for name, df in dfs.items()})
sns.boxplot(data=queue_data, ax=axes2[1])
axes2[1].set_title("Распределение длин очередей")
axes2[1].set_ylabel("Кол-во ТС")
# ИСПРАВЛЕНО: Безопасный поворот подписей
axes2[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig("zcombineplots32.png", dpi=200)

# 4. Сводная таблица (средние значения за весь период)
summary = pd.DataFrame({name: df.mean() for name, df in dfs.items()}).T
# Удаляем техническую колонку времени из сводной таблицы, так как её среднее не информативно
if "time" in summary.columns:
    summary = summary.drop(columns=["time"])

print("--- Сводная таблица средних показателей ---")
print(summary)
summary.to_csv("zcombineplots3.csv")

plt.show()