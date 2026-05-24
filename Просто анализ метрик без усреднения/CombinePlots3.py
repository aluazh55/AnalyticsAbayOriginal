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

# Загрузка
dfs = {name: pd.read_csv(path) for name, path in scenarios.items() if os.path.exists(path)}

# 2. Построение графиков сравнения во времени
PLOTS = [
    ("travel_time", "Время (с)", "Среднее время в пути"),
    ("queue", "Кол-во ТС", "Длина очередей"),
    ("throughput", "Транспортных средств/мин", "Пропускная способность"),
    ("speed", "м/с", "Средняя скорость"),
    ("spillback", "Кол-во событий", "Инциденты заторов (Spillback)"),
    ("co2_rate_mg", "мг/мин", "Выбросы CO2"),
]

fig, axes = plt.subplots(3, 2, figsize=(16, 15))
fig.suptitle("Анализ эффективности алгоритмов управления", fontsize=18)

for ax, (col, ylabel, title) in zip(axes.flat, PLOTS):
    for name, df in dfs.items():
        ax.plot(df["time"], df[col], label=name, alpha=0.8)
    ax.set_title(title, fontsize=12)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(fontsize=8)

plt.subplots_adjust(hspace=0.4, wspace=0.3, top=0.92)
plt.savefig("zcombineplots31.png", dpi=200)

# 3. Статистический анализ (Box Plots для сравнения стабильности)
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))
# Сравнение скоростей
speed_data = pd.DataFrame({name: df["speed"] for name, df in dfs.items()})
sns.boxplot(data=speed_data, ax=axes2[0])
axes2[0].set_title("Распределение скоростей")
axes2[0].set_ylabel("м/с")

# Сравнение очередей
queue_data = pd.DataFrame({name: df["queue"] for name, df in dfs.items()})
sns.boxplot(data=queue_data, ax=axes2[1])
axes2[1].set_title("Распределение длин очередей")
axes2[1].set_ylabel("Кол-во ТС")

plt.tight_layout()
plt.savefig("zcombineplots32.png", dpi=200)

# 4. Сводная таблица (средние значения)
summary = pd.DataFrame({name: df.mean() for name, df in dfs.items()}).T
print("--- Сводная таблица средних показателей ---")
print(summary)
summary.to_csv("zcombineplots3.csv")

plt.show()