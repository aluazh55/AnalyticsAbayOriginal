import pandas as pd
import matplotlib.pyplot as plt
import os

# Список файлов, которые вы сгенерировали
scenarios = {
    "NoAlgo": "metrics_NoAlgo.csv",
    "Gridlock": "metrics_mpc_Gridlock.csv",
    "OffsetSplit": "metrics_OffsetSplit.csv",
    "OffsetOnly": "metrics_OffsetOnly.csv"
}

# Загрузка данных (только если файлы существуют)
dfs = {name: pd.read_csv(path) for name, path in scenarios.items() if os.path.exists(path)}

if not dfs:
    print("Ошибка: CSV файлы не найдены. Сначала запустите симуляции.")
    exit()

PLOTS = [
    ("travel_time", "Avg Travel Time (s)", "Время в пути"),
    ("queue", "Total Queue Length (veh)", "Длина очередей"),
    ("throughput", "Vehicles/min", "Пропускная способность"),
    ("speed", "Mean Speed (m/s)", "Средняя скорость"),
    ("spillback", "Spillback Events", "Инциденты заторов"),
    ("co2_rate_mg", "CO2 Emission (mg/min)", "Выбросы CO2"),
]

fig, axes = plt.subplots(3, 2, figsize=(15, 12))
fig.suptitle("Сравнение сценариев управления коридором", fontsize=16)

for ax, (col, ylabel, title) in zip(axes.flat, PLOTS):
    for name, df in dfs.items():
        ax.plot(df["time"], df[col], label=name, linewidth=1.5)

    ax.set_title(title)
    ax.set_xlabel("Время симуляции (с)")
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("simulation_comparison.png", dpi=200)
plt.show()
