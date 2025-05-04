import matplotlib.pyplot as plt
conf = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

data = {
    'A1': {
        'f1': [0.9655,0.9655,0.9286,0.6957,0.1250,0,0,0,0,0],
        'prec': [1.0000, 1.0000,1.0000,1.0000,1.0000,0,0,0,0,0],
        'rec': [0.9333,0.9333,0.8667,0.5333,0.0667,0,0,0,0,0]
    },
    'A3': {
        'f1': [0.9375,0.9375,0.9677,0.9375,0.8000,0,0,0,0,0],
        'prec': [0.8824,0.8824,0.9375,0.8824,1.0000,0,0,0,0,0],
        'rec': [1.0000,1.0000, 1.0000,1.0000,0.6667,0,0,0,0,0]
    },
    'A5': {
        'f1': [0.6122,0.6122,0.7317,0.9091,0.5714,0,0,0,0,0],
        'prec': [0.4412,0.4412,0.5769,0.8333,1.0000,0,0,0,0,0],
        'rec': [1,1,1,1,0.4000,0,0,0,0,0]
    },
    'A7': {
        'f1': [0.7500, 0.7500,0.6957,0.5714,0.3333,0,0,0,0,0],
        'prec': [1.0000,1.0000,1.0000,1.0000,1.0000,0,0,0,0,0],
        'rec': [0.6000,0.6000,0.5333,0.4000,0.2000,0,0,0,0,0]
    },
    'A9': {
        'f1': [0.5806,0.5806,0.2727,0.1905,0,0,0,0,0,0],
        'prec': [0.5625,0.5625,0.4286,0.3333,0,0,0,0,0,0],
        'rec': [0.6000, 0.6000,0.2000,0.1333,0,0,0,0,0,0]
    },
    'C1': {
        'f1': [0.5714,0.5714, 0.4211,0.3333,0,0,0,0,0,0],
        'prec': [1.0000,1.0000,1.0000,1.0000,0,0,0,0,0,0],
        'rec': [ 0.4000,0.4000,0.2667,0.2000,0,0,0,0,0,0]
    },
    'C3': {
        'f1': [1.0000,1.0000,1.0000,1.0000,0.8000,0,0,0,0,0],
        'prec': [1.0000,1.0000,1.0000,1.0000,1.0000,0,0,0,0,0],
        'rec': [1.0000,1.0000,1.0000,1.0000,0.6667,0,0,0,0,0]
    },
    'C5': {
        'f1': [1.0000,1.0000,1.0000,1.0000,0.5714,0,0,0,0,0],
        'prec': [1.0000,1.0000,1.0000,1.0000,1.0000,0,0,0,0,0],
        'rec': [1.0000,1.0000,1.0000,1.0000,0.4000,0,0,0,0,0]
    },
    'C7': {
        'f1': [0.6087,0.6087,0.6364,0.5714,0.3333,0,0,0,0,0],
        'prec': [0.8750,0.8750,1.0000,1.0000,1.0000,0,0,0,0,0],
        'rec': [0.4667,0.4667,0.4667, 0.4000,0.2000,0,0,0,0,0]
    },
    'C9': {
        'f1': [0.7222,0.7222,0.7273,0.6400,0.3333,0,0,0,0,0],
        'prec': [0.6190,0.6190,0.6667,0.8000,1.0000,0,0,0,0,0],
        'rec': [0.8667,0.8667,0.8000,0.5333, 0.2000,0,0,0,0,0]
    },
    'E1': {
        'f1': [0.3750,0.3750,0.4167,0.3333,0.1250,0,0,0,0,0],
        'prec': [0.3529,0.3529,0.5556,1.0000,1.0000,0,0,0,0,0],
        'rec': [0.4000,0.4000,0.3333,0.2000,0,0,0,0,0,0]
    },
    'E3': {
        'f1': [0.6977,0.6977,0.8000,0.9655,0.8889,0.2353,0,0,0,0],
        'prec': [0.5357,0.5357, 0.7000,1.0000,1.0000,1.0000,0,0,0,0],
        'rec': [1.0000,1.0000,0.9333,0.9333,0.8000,0.1333,0,0,0,0]
    },
    'E5': {
        'f1': [0.3768,0.3768,0.4906,0.7273,0.5000,0,0,0,0,0],
        'prec': [0.2407,0.2407,0.3421,0.6667,1.0000,0,0,0,0,0],
        'rec': [0.8667,0.8667,0.8667,0.8000, 0.3333, 0,0,0,0,0]
    },
    'E7': {
        'f1': [0.2963,0.2963,0.4000,0.5882,0.6923,0,0,0,0,0],
        'prec': [0.1818,0.1818,0.2667,0.5263,0.8182,0,0,0,0,0],
        'rec': [0.8000,0.8000,0.8000,0.6667, 0.6000,0,0,0,0,0]
    },
    'E9': {
        'f1': [ 0.8000,0.8000,0.8667,0.8148,0.5714,0,0,0,0,0],
        'prec': [0.7000,0.7000,0.8667,0.9167,1.0000,0,0,0,0,0],
        'rec': [0.9333,0.9333,0.8667,0.7333,0.4000,0,0,0,0,0]
    }
}

import matplotlib.pyplot as plt

# === Gemeinsame Variablen ===
conf = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

# === plot_group() mit Speicherung ===
def plot_group(prefix, output_path):
    fig = plt.figure(figsize=(8, 16))
    gs = fig.add_gridspec(5, 1)

    for idx, suffix in enumerate(['1', '3', '5', '7', '9']):
        ax = fig.add_subplot(gs[idx, 0])
        key = prefix + suffix

        ax.plot(conf, data[key]['f1'],'o-', label='F1-Score')
        ax.plot(conf, data[key]['prec'],'o-', label='Precision')
        ax.plot(conf, data[key]['rec'],'o-', label='Recall')

        ax.set_title(f'{key}', fontsize=16)
        ax.set_xlabel("Confidence", fontsize=16)
        ax.set_ylim(0, 1.1)
        ax.grid(True)
        ax.tick_params(axis='both', labelsize=14)
        ax.set_ylabel("Score", fontsize=16)
        ax.legend(loc='lower right', fontsize=14)

    plt.tight_layout()
    plt.savefig(output_path, format="svg")
    plt.close()

# === plot_all_groups_vertical() mit Speicherung ===
def plot_all_groups_vertical(output_path):
    groups = ['A', 'C', 'E']
    suffixes = ['1', '3', '5', '7', '9']

    fig, axes = plt.subplots(5, 3, figsize=(18, 18), sharex=True, sharey=True)

    for col, group in enumerate(groups):
        for row, suffix in enumerate(suffixes):
            key = group + suffix
            ax = axes[row, col]

            ax.plot(conf, data[key]['f1'],'o-', label='F1-Score')
            ax.plot(conf, data[key]['prec'],'o-', label='Precision')
            ax.plot(conf, data[key]['rec'],'o-', label='Recall')

            ax.set_title(f'{key}', fontsize=13)
            ax.set_ylim(0, 1.1)
            ax.grid(True)
            ax.tick_params(axis='both', labelsize=11)

            if col == 0:
                ax.set_ylabel("Score", fontsize=12)
            if row == 4:
                ax.set_xlabel("Confidence", fontsize=12)
            if row == 4 and col == 2:
                ax.legend(loc='lower right', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, format="svg")
    plt.close()

# === Aufruf der Funktionen ===
plot_group('A', "group_A.svg")
plot_group('C', "group_C.svg")
plot_group('E', "group_E.svg")
plot_all_groups_vertical("all_groups_vertical.svg")
