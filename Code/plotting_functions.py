import matplotlib.pyplot as plt
import os
import ast

def plot_hits(timestamps, raw_hits, smoothed_hits, grouped_timestamps, grouped_hits, csv_path):
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, raw_hits, label="Raw Hits", linestyle='dashed', marker='o', alpha=0.5)
    plt.plot(timestamps, smoothed_hits, label="Smoothed Hits", linestyle='solid', marker='x', alpha=0.8)
    plt.stem(grouped_timestamps, grouped_hits, label="Grouped Hits", linefmt=":", markerfmt="*")
    plt.xlabel("Timestamp (s)")
    plt.ylabel("Hit Detection (0/1)")
    plt.title("Raw vs. Smoothed Hits")
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(os.path.join(csv_path, "hits_plot.png"))
    plt.close()

def plot_grouped_hits(timestamps, grouped_hits, csv_path):
    plt.figure(figsize=(10, 4))
    plt.stem(timestamps, grouped_hits, label='Grouped Hits', linefmt=':')
    plt.xlabel("Timestamp (s)")
    plt.ylabel("Hit Detected (1 = Hit, 0 = No Hit)")
    plt.title("Grouped Hits Over Time")
    plt.legend()
    plt.grid()
    plt.show()
    plt.savefig(os.path.join(csv_path, "hits_plot_grouped.png"))
    plt.close()

def plot_grouped_hits_xy(df_grouped, csv_path):
    raw_positions = df_grouped["Position (x, y) in cm"].tolist()
    positions = []

    for p in raw_positions:
        if isinstance(p, str):
            try:
                p = ast.literal_eval(p)
            except Exception as e:
                print(f"Fehler beim Parsen der Position: {p} → {e}")
                continue
        positions.append(p)

    if not all(isinstance(p, tuple) and len(p) == 2 for p in positions):
        print(f"Fehler: Ungültiges Format für Positionsdaten: {positions}")
        return

    x_values, y_values = zip(*positions)

    plt.figure(figsize=(8, 6))
    plt.scatter(x_values, y_values, color='blue', label='Grouped Hits')

    for i, (x, y) in enumerate(positions, start=1):
        plt.text(x, y, str(i), fontsize=12, ha='right', va='bottom', color='black')

    plt.xlabel("X-Position (cm)")
    plt.ylabel("Y-Position (cm)")
    plt.title("Grouped Hits with Numbering")
    plt.xlim(0, 200)
    plt.xticks(range(0, 200, 20))
    plt.ylim(0, 120)
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(csv_path, "hits_plot_grouped_xy.png"))
    plt.show()
    plt.close()
