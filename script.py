import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)

folder_path = os.path.join(base_dir, 'output')
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

plot_folder = os.path.join(base_dir, 'plots')
os.makedirs(plot_folder, exist_ok=True)

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)

    # Replace "CWE-" followed by a space with an empty string
    df['CWEs'] = df['CWEs'].str.replace('CWE- ', '')

    # Exclude missing values (NaN) before sorting
    df = df.dropna(subset=['CWEs'])

    unique_labels = df['CWEs'].unique()

    # Plot histogram
    fig, ax = plt.subplots(figsize=(13, 9))
    counts = df['CWEs'].value_counts()
    ax.bar(counts.index, counts.values, width=0.5)  # Use bar plot instead of hist

    plt.title(f'Histogram for {os.path.splitext(file)[0]}')
    plt.xlabel('CWEs')
    plt.ylabel('Frequency')

    # Increase spacing between x-axis labels
    plt.xticks(rotation=45, ha='center', fontsize=8)  # Set rotation angle to 90 degrees

    # Save the plot as a JPEG file
    plot_name = f"{os.path.splitext(file)[0]}.jpeg"
    plot_path = os.path.join(plot_folder, plot_name)
    plt.savefig(plot_path, format='jpeg')

    # Display a message indicating the saved file
    print(f"Saved plot: {plot_path}")

    # Close the plot
    plt.close()
