import pandas as pd
import matplotlib.pyplot as plt

algorithms = ['OffsetOnly', 'OffsetSplit', 'Gridlock', 'NoAlgo']
jab_phases = [
    "ggggrrrrrrggggrrrrrrr", "yyyyrrrrrrggggrrrrrrr", "rrrrrrrrrrggggggrrrrr",
    "rrrrrrrrrrgyyyyyrrrrr", "rrrrrrgggggrrrrrggggg", "rrrrrrggyygrrrrryyyyy",
    "ggggggggrrgrrrrrrrrrr", "ggggyyyyrrgrrrrrrrrrr"
]

fig, axes = plt.subplots(4, 1, figsize=(14, 20))

for idx, algo in enumerate(algorithms):
    ax = axes[idx]

    # Read log
    df = pd.read_csv(f'phase{algo}_log_Jab.csv')
    df = df[df['state'].isin(jab_phases)].copy()

    # Increment cycle counter each time the main starting phase is encountered
    df['cycle'] = (df['state'] == jab_phases[0]).cumsum()

    # Map durations against cycles
    pivot_df = df.pivot_table(index='cycle', columns='state', values='duration', aggfunc='sum')

    # Plot each phase sequence
    for phase in jab_phases:
        if phase in pivot_df.columns:
            ax.plot(pivot_df.index, pivot_df[phase], marker='o', markersize=4, label=phase)

    ax.set_title(f'Duration of Each Phase per Cycle - Jab ({algo} Algorithm)', fontsize=14)
    ax.set_xlabel('Amount of Full Cycles', fontsize=12)
    ax.set_ylabel('Duration (Seconds)', fontsize=12)
    ax.set_ylim(0, 100)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('jab_cycle_durationsJab.png', bbox_inches='tight')