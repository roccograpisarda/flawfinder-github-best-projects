import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = os.path.join(base_dir, 'output')
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

plot_folder = os.path.join(base_dir, 'plots')
os.makedirs(plot_folder, exist_ok=True)

threshold = 3.50

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)

    # Convert 'CWEs' column to string
    df['CWEs'] = df['CWEs'].astype(str)

    # Exclude missing values (NaN) before sorting
    df = df.dropna(subset=['CWEs'])

    # Plot histogram
    fig, ax = plt.subplots(figsize=(11, 7))
    counts = df['CWEs'].value_counts()
    ax.bar(counts.index, counts.values, width=0.5)  # Use bar plot instead of hist
    
    plt.xlabel("CWEs", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    # Increase spacing between x-axis labels
    plt.xticks(rotation=0, ha='center', fontsize=8)  # Set rotation angle to 90 degrees

    # Save the plot as a JPEG file
    plot_name = f"{os.path.splitext(file)[0]}_bar.png"
    plot_path = os.path.join(plot_folder, plot_name)
    plt.savefig(plot_path, format='png')
    # Close the plot
    plt.close()

    # Plot pie chart
    fig, ax = plt.subplots(figsize=(10, 10))
    counts = df['CWEs'].value_counts()
    percentages = counts.values / counts.values.sum() * 100

    # Filter labels based on the threshold
    labels = counts.index[percentages >= threshold]
    filtered_percentages = percentages[percentages >= threshold]

    # Calculate the sum of values below the threshold
    other_label = 'Others'
    other_percentage = percentages[percentages < threshold].sum()

    # Only include the "Others" category if its percentage is above 0.0%
    if other_percentage > 0.0:
        labels = labels.append(pd.Index([other_label]))
        filtered_percentages = pd.Series(filtered_percentages)._append(pd.Series([other_percentage]))

        wedges, text, autotext = ax.pie(filtered_percentages, labels=None, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},
                                        autopct='%1.1f%%', startangle=90)

        # Create a legend
        legend_labels = [f"{label}: {percentage:.1f}%" for label, percentage in zip(labels, filtered_percentages)]
        plt.legend(wedges, legend_labels, loc='best', bbox_to_anchor=(1.1, 1))
    else:
        wedges, text, autotext = ax.pie(filtered_percentages, labels=None, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},
                                        autopct='%1.1f%%', startangle=90)
                # Create a legend
        legend_labels = [f"{label}: {percentage:.1f}%" for label, percentage in zip(labels, filtered_percentages)]
        plt.legend(wedges, legend_labels, loc='best', bbox_to_anchor=(1.1, 1))

    # Save the plot as a JPEG file with the legend included
    plot_with_legend_name = f"{os.path.splitext(file)[0]}_pie.png"
    plot_with_legend_path = os.path.join(plot_folder, plot_with_legend_name)
    plt.savefig(plot_with_legend_path, format='png', bbox_inches='tight')
    # Close the plot
    plt.close()



print("Created all the plots for the CSV files in the output folder")
