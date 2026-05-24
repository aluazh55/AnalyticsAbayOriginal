import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def plot_real_traffic_wave(algo_name, time_limit=600, v_kmh=50):
    """
    Reads simulation CSVs and generates a Time-Space diagram.
    """
    v_ms = v_kmh / 3.6

    # Cumulative distances along the corridor (adjust based on real map data)
    distances = {'Jab': 0, 'Jam': 300, 'Jas': 600}

    # Исправленный словарь: фазы обернуты в списки []
    phases = {
        'Jab': {
            'green': ['ggggrrrrrrggggrrrrrrr',
                      'yyyyrrrrrrggggrrrrrrr', 'rrrrrrrrrrggggggrrrrr'],
            # End is just left turn rrrrrrrrrrggggggrrrrr
            'red': ['rrrrrrgggggrrrrrggggg']
        },
        'Jam': {
            'green': ['ggggggrrrrggggggrrrr'],
            'red': ['rrrrrrggggrrrrrrgggg', 'rrrrrrrrrrrrrrrrrrrr']
        },
        'Jas': {
            'green': ['gggggrrrrrrrgggggrrrrrrr', 'yyyyyrrrrrrrgggggrrrrrrr', 'rrrrrrrrrrrrggggggrrrrrr'],
            # End is just left turn rrrrrrrrrrrrggggggrrrrrr Green considered only from WE, туда может попасть зеленый с другого направления, но смотрится только по WE
            'red': ['rrrrrrggggggrrrrrrgggggg', 'rrrrrrggggggrrrrrryyyyyy', 'rrrrrrggggggrrrrrrrrrrrr']
        }
    }

    fig, ax = plt.subplots(figsize=(14, 8))

    # 1. Plot the traffic light states
    for junc in ['Jab', 'Jam', 'Jas']:
        # Load the corresponding CSV
        filename = f'phase{algo_name}_log_{junc}.csv'
        df = pd.read_csv(filename)

        # Filter for the timeframe we want to view
        df = df[df['t_start'] <= time_limit]

        y_pos = distances[junc]

        for _, row in df.iterrows():
            state = row['state']
            t = row['t_start']
            dur = row['duration']

            # Проверяем нахождение фазы в списке через 'in'
            if state in phases[junc]['green']:
                color, alpha = '#2ecc71', 0.8  # Solid Green
            elif state in phases[junc]['red']:
                color, alpha = '#e74c3c', 0.8  # Solid Red
            else:
                color, alpha = '#f1c40f', 0.4  # Yellow for transitions/other phases

            # Draw the signal phase block
            ax.broken_barh([(t, dur)], (y_pos - 15, 30),
                           facecolors=color, alpha=alpha, edgecolor='black', linewidth=0.5)

        # Label the intersection on the Y-axis
        ax.text(-15, y_pos, f'{junc}', va='center', ha='right', fontweight='bold', fontsize=12)

    # 2. Draw vehicle trajectories (Green Wave platoons)
    jab_df = pd.read_csv(f'phase{algo_name}_log_Jab.csv')

    # Исправлена логика выборки, так как green теперь список
    jab_greens = jab_df[(jab_df['state'].isin(phases['Jab']['green'])) & (jab_df['t_start'] <= time_limit)]

    for _, row in jab_greens.iterrows():
        # Start a platoon 5 seconds after Jab turns green (reaction time/start-up delay)
        start_time = row['t_start'] + 5

        # Calculate time to reach the last intersection at constant speed
        end_time = start_time + (distances['Jas'] / v_ms)

        # Plot the trajectory line
        ax.plot([start_time, end_time], [distances['Jab'], distances['Jas']],
                color='blue', linewidth=2, alpha=0.7)

    # 3. Graph formatting
    ax.set_title(f'Time-Space Diagram (Green Wave Progression) - Algorithm: {algo_name}', fontsize=16)
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Distance along corridor (meters)', fontsize=12)
    ax.set_xlim(0, time_limit)
    ax.set_ylim(-50, max(distances.values()) + 100)
    ax.grid(True, linestyle='--', alpha=0.5)

    # Add a clean legend
    legend_elements = [
        Patch(facecolor='#2ecc71', label='Main Target Green Phase'),
        Patch(facecolor='#e74c3c', label='Main Target Red Phase'),
        Patch(facecolor='#f1c40f', label='Transitions (Yellow/Other)'),
        plt.Line2D([0], [0], color='blue', lw=2, label=f'Vehicle Trajectory ({v_kmh} km/h)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig('Offset_OffsetSplit.png', bbox_inches='tight')



# Запуск
plot_real_traffic_wave("OffsetSplit")