import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = os.path.join(base_dir, 'output')
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

plot_folder = os.path.join(base_dir, 'plots')
os.makedirs(plot_folder, exist_ok=True)

threshold = 3.50

project_cwes = {}  # Dictionary to store CWEs and counts for each project

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)

    # Convert 'CWEs' column to string
    df['CWEs'] = df['CWEs'].astype(str)

    # Exclude missing values (NaN) before sorting
    df = df.dropna(subset=['CWEs'])

    # Collect CWEs and counts for the project
    project_name = os.path.splitext(file)[0]
    counts = df['CWEs'].value_counts()
    project_cwes[project_name] = counts

    # Plot histogram
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.bar(counts.index, counts.values, width=0.5)  # Use bar plot instead of hist

    plt.xlabel("CWEs", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    # Increase spacing between x-axis labels
    plt.xticks(rotation=0, ha='center', fontsize=8)  # Set rotation angle to 90 degrees

    # Save the plot as a JPEG file
    plot_name = f"{project_name}_bar.png"
    plot_path = os.path.join(plot_folder, plot_name)
    plt.savefig(plot_path, format='png')
    # Close the plot
    plt.close()

# Create a grouped chart
fig, ax = plt.subplots(figsize=(12, 8))

project_names = list(project_cwes.keys())
bar_width = 0.4 / len(project_names)  # Adjust the bar width here
padding = (0.4 - (bar_width * len(project_names))) / 2
bar_positions = []

max_count = max([counts.max() for counts in project_cwes.values()])
y_axis_limit = max_count * 1.2  # Increase the y-axis limit by 20% for better visibility of low counts

all_cwes = pd.concat(list(project_cwes.values()))  # Combine counts for all projects
unique_cwes = all_cwes.index.unique()  # Get unique CWEs across all projects

for i, project_name in enumerate(project_names):
    counts = project_cwes[project_name]
    bar_position = [j + padding + (i * bar_width) for j in range(len(unique_cwes))]
    bar_positions.append(bar_position)

    # Fill missing counts with 0 for the project
    counts = counts.reindex(unique_cwes, fill_value=0)

    ax.bar(bar_position, counts.values, width=bar_width, alpha=0.7, label=project_name)

    # Add labels with quantity above each bar
    for x, y in zip(bar_position, counts.values):
        ax.text(x, y, str(y), ha='center', va='bottom')

plt.xlabel("CWEs", fontsize=12)
plt.ylabel("Frequency", fontsize=12)

# Set x-axis tick positions and labels
tick_positions = [pos + (0.4 / len(project_names)) / 2 for pos in range(len(unique_cwes))]
ax.set_xticks(tick_positions)
ax.set_xticklabels(unique_cwes, rotation=0, ha='center', fontsize=8)

# Center the ticks
ax.tick_params(axis='x', pad=10)

# Set y-axis limits
plt.ylim(0, y_axis_limit)

plt.legend()

# Save the grouped chart as a JPEG file
grouped_chart_path = os.path.join(plot_folder, 'grouped_chart.png')
plt.savefig(grouped_chart_path, format='png')
# Close the plot
plt.close()

print("Created all the plots for the CSV files in the output folder")
