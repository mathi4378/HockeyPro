import os
import numpy as np
import pandas as pd
from scipy.signal import medfilt

from plotting_functions import plot_hits
from plotting_functions import plot_grouped_hits
from plotting_functions import plot_grouped_hits_xy


def sliding_window_threshold(data, window_size, low_threshold, high_threshold):
    windows = np.lib.stride_tricks.sliding_window_view(data, window_size)
    smoothed = np.mean(windows, axis=1)
    result = np.zeros(len(data), dtype=int)
    # Hysterese-Logik
    previous_value = 0
    for i, value in enumerate(smoothed, start=window_size // 2):
        if value >= high_threshold:
            previous_value = 1
        elif value <= low_threshold:
            previous_value = 0
        result[i] = previous_value
    return result


def group_filter(signal, timestamps, positions):
    grouped_timestamps = []
    grouped_positions = []
    new_signal = np.zeros_like(signal)

    current_timestamps = []
    current_positions = []
    segment_indices = []

    for i in range(len(signal)):
        if signal[i] == 1:
            if positions[i] is not None and positions[i] != (None, None):
                current_timestamps.append(timestamps[i])
                current_positions.append(positions[i])
                segment_indices.append(i)
        elif signal[i] == 0 and current_timestamps:
            # Ersten Wert des Segments nehmen
            first_timestamp = current_timestamps[0]
            first_position = current_positions[0]

            # Setze ersten Wert in die Mitte des Segments
            mid_index = segment_indices[len(segment_indices) // 2]
            timestamps[mid_index] = first_timestamp
            positions[mid_index] = first_position

            # Restliche Werte des Segments beibehalten
            grouped_timestamps.append(first_timestamp)
            grouped_positions.append(first_position)
            for idx in segment_indices:
                new_signal[idx] = 1  # Erhalte die 1 in der neuen Liste


            current_timestamps = []
            current_positions = []
            segment_indices = []
        else:
            new_signal[i] = signal[i]  # Unveränderte Werte übernehmen

    # Falls das Signal mit 1 endet
    if current_timestamps:
        avg_timestamp = np.mean(current_timestamps)
        avg_position = tuple(np.mean(current_positions, axis=0)) if current_positions else (None, None)
        mid_index = segment_indices[len(segment_indices) // 2]
        timestamps[mid_index] = avg_timestamp
        positions[mid_index] = avg_position
        grouped_timestamps.append(avg_timestamp)
        grouped_positions.append(avg_position)
        for idx in segment_indices:
            new_signal[idx] = 1

    return grouped_timestamps, grouped_positions, new_signal

def signal_process(hit_data, timestamps, positions, method, window_size, low_threshold, high_threshold,csv_path):
    RESULTS_DIR = csv_path
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if method not in ["moving_average", "sliding_window_threshold"]:
        raise ValueError(f"Die gewählte Methode '{method}' wird nicht unterstützt")

    if len(hit_data) < window_size:
        raise ValueError("Fenstergröße ist größer als die Anzahl der Datenpunkte")

    # Initialisiere smoothed_hits, um sicherzustellen, dass es nicht ungebunden bleibt
    smoothed_hits = np.zeros_like(hit_data)

    smoothed_hits = sliding_window_threshold(hit_data, window_size, low_threshold, high_threshold)

    min_length = min(len(smoothed_hits), len(timestamps), len(positions), len(hit_data))
    timestamps = timestamps[:min_length]
    positions = positions[:min_length]
    smoothed_hits = smoothed_hits[:min_length]
    hit_data = hit_data[:min_length]

    # Segmentiere und mittlere x, y und Zeitwerte für grouped hits
    grouped_timestamps, grouped_positions, new_signal = group_filter(smoothed_hits, timestamps, positions)

    df_smoothed = pd.DataFrame({
        "Hit": smoothed_hits.tolist(),
        "Position (x, y) in cm": [f"({pos[0]:.5f}, {pos[1]:.5f})" if pos and pos != (None, None) else "(None, None)" for
                                  pos in positions],
        "Timestamp (s)": [f"{ts:.5f}" for ts in timestamps]
    })

    smoothed_csv_path = os.path.join(RESULTS_DIR, "smoothed_hits.csv")
    df_smoothed.to_csv(smoothed_csv_path, index=False)
    print(f"Geglättete Treffer gespeichert als '{smoothed_csv_path}'")

    df_grouped = pd.DataFrame({
        "Hit": [1] * len(grouped_timestamps),
        "Position (x, y) in cm": [(pos[0], pos[1]) if pos and pos != (None, None) else (None, None)
                           for pos in grouped_positions],
        "Timestamp (s)": [(ts, 5) for ts in grouped_timestamps],

    })

    grouped_csv_path = os.path.join(RESULTS_DIR, "grouped_hits.csv")
    df_grouped.to_csv(grouped_csv_path, index=False)
    print(f"Gruppierte Treffer gespeichert als '{grouped_csv_path}'")

    plot_hits(timestamps, hit_data, smoothed_hits,grouped_timestamps,[1.5] * len(grouped_timestamps),csv_path) # Plotte die geglätteten Treffer
    plot_grouped_hits(grouped_timestamps, [1] * len(grouped_timestamps),csv_path)  # Binäres Signal über Zeit plotten
    plot_grouped_hits_xy(df_grouped,csv_path)  # Plotte x- und y-Werte der Grouped Hits mit Nummerierung

    return df_smoothed, df_grouped
