import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Загрузка данных
scenarios = {
    "NoAlgo": "metrics_NoAlgo.csv",
    "Gridlock": "metrics_mpc_Gridlock.csv",
    "OffsetSplit": "metrics_OffsetSplit.csv",
    "OffsetOnly": "metrics_OffsetOnly.csv"
}
dfs = {name: pd.read_csv(path) for name, path in scenarios.items() if os.path.exists(path)}

# 1. Вычисляем средние значения
summary = pd.DataFrame({name: df.mean() for name, df in dfs.items()}).T

# 2. Выбираем колонки и переименовываем их для отображения на графике
metrics_map = {
    "travel_time": "Время в пути (с)",
    "speed": "Скорость (м/с)",
    "co2_rate_mg": "Выбросы CO2",
    "queue": "Длина очереди",
    "throughput": "Пропускная способность"
}
data_subset = summary[list(metrics_map.keys())].rename(columns=metrics_map)

# Переименовываем сценарии (строки)
scenarios_map = {
    "NoAlgo": "Без Алгоритма",
    "Gridlock": "Gridlock",
    "OffsetSplit": "Offset Split",
    "OffsetOnly": "Только Offset"
}
data_subset.rename(index=scenarios_map, inplace=True)

# 3. Нормализация (Min-Max)
normalized_data = (data_subset - data_subset.min()) / (data_subset.max() - data_subset.min())

# 4. Визуализация
plt.figure(figsize=(10, 10))
# Используем annot=data_subset для отображения реальных цифр
sns.heatmap(normalized_data, annot=data_subset, fmt=".1f", cmap="RdYlGn_r", linewidths=0.5)

plt.title("Сравнительная матрица эффективности алгоритмов", fontsize=14)
plt.ylabel("Сценарии")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig("zheatmap_comparison_ru.png", dpi=200)
plt.show()