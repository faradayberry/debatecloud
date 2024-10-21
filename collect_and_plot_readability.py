import subprocess
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import re
import json
import os

# Define the list of debates with their parameters
debates = [
    {'year': 1960, 'suffix': 'a', 'candidates': ['Kennedy', 'Nixon'], 'colors': ['blue', 'red']},
    {'year': 1960, 'suffix': 'b', 'candidates': ['Kennedy', 'Nixon'], 'colors': ['blue', 'red']},
    {'year': 1960, 'suffix': 'c', 'candidates': ['Kennedy', 'Nixon'], 'colors': ['blue', 'red']},
    {'year': 1976, 'suffix': 'a', 'candidates': ['Carter', 'Ford'], 'colors': ['blue', 'red']},
    {'year': 1976, 'suffix': 'b', 'candidates': ['Carter', 'Ford'], 'colors': ['blue', 'red']},
    {'year': 1976, 'suffix': 'c', 'candidates': ['Carter', 'Ford'], 'colors': ['blue', 'red']},
    {'year': 1980, 'suffix': None, 'candidates': ['Carter', 'Reagan'], 'colors': ['blue', 'red']},
    {'year': 1984, 'suffix': 'a', 'candidates': ['Mondale', 'Reagan'], 'colors': ['blue', 'red']},
    {'year': 1984, 'suffix': 'b', 'candidates': ['Mondale', 'Reagan'], 'colors': ['blue', 'red']},
    {'year': 1988, 'suffix': 'a', 'candidates': ['Dukakis', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 1988, 'suffix': 'b', 'candidates': ['Dukakis', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 1992, 'suffix': 'a', 'candidates': ['Clinton', 'Bush', 'Perot'], 'colors': ['blue', 'red', 'green']},
    {'year': 1992, 'suffix': 'b', 'candidates': ['Clinton', 'Bush', 'Perot'], 'colors': ['blue', 'red', 'green']},
    {'year': 1992, 'suffix': 'c', 'candidates': ['Clinton', 'Bush', 'Perot'], 'colors': ['blue', 'red', 'green']},
    {'year': 1996, 'suffix': 'a', 'candidates': ['Clinton', 'Dole'], 'colors': ['blue', 'red']},
    {'year': 1996, 'suffix': 'b', 'candidates': ['Clinton', 'Dole'], 'colors': ['blue', 'red']},
    {'year': 2000, 'suffix': 'a', 'candidates': ['Gore', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 2000, 'suffix': 'b', 'candidates': ['Gore', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 2000, 'suffix': 'c', 'candidates': ['Gore', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 2004, 'suffix': 'a', 'candidates': ['Kerry', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 2004, 'suffix': 'b', 'candidates': ['Kerry', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 2004, 'suffix': 'c', 'candidates': ['Kerry', 'Bush'], 'colors': ['blue', 'red']},
    {'year': 2008, 'suffix': 'a', 'candidates': ['Obama', 'McCain'], 'colors': ['blue', 'red']},
    {'year': 2008, 'suffix': 'b', 'candidates': ['Obama', 'McCain'], 'colors': ['blue', 'red']},
    {'year': 2008, 'suffix': 'c', 'candidates': ['Obama', 'McCain'], 'colors': ['blue', 'red']},
    {'year': 2012, 'suffix': 'a', 'candidates': ['Obama', 'Romney'], 'colors': ['blue', 'red']},
    {'year': 2012, 'suffix': 'b', 'candidates': ['Obama', 'Romney'], 'colors': ['blue', 'red']},
    {'year': 2012, 'suffix': 'c', 'candidates': ['Obama', 'Romney'], 'colors': ['blue', 'red']},
    {'year': 2016, 'suffix': 'a', 'candidates': ['Clinton', 'Trump'], 'colors': ['blue', 'red']},
    {'year': 2016, 'suffix': 'b', 'candidates': ['Clinton', 'Trump'], 'colors': ['blue', 'red']},
    {'year': 2016, 'suffix': 'c', 'candidates': ['Clinton', 'Trump'], 'colors': ['blue', 'red']},
    {'year': 2020, 'suffix': 'a', 'candidates': ['Biden', 'Trump'], 'colors': ['blue', 'red']},
    {'year': 2020, 'suffix': 'b', 'candidates': ['Biden', 'Trump'], 'colors': ['blue', 'red']},
    {'year': 2024, 'suffix': 'a', 'candidates': ['Biden', 'Trump'], 'colors': ['blue', 'red']},
    {'year': 2024, 'suffix': 'b', 'candidates': ['Harris', 'Trump'], 'colors': ['blue', 'red']},
]


# Metrics to analyze
metrics = [
    'Flesch-Kincaid Grade Level',
    'Gunning Fog Index',
    'Simple Measure of Gobbledygook',
    'Coleman-Liau Index'
]

# Filename to save and load the collected scores
results_filename = 'readability_scores_over_time.json'

# Check if the results file exists
if os.path.exists(results_filename):
    print(f"Loading results from {results_filename}...")
    with open(results_filename, 'r') as f:
        scores_over_time = json.load(f)
else:
    print("Results file not found. Running analysis...")
    # Dictionary to store scores
    scores_over_time = {metric: {'blue': {}, 'red': {}} for metric in metrics}

    # Collect readability scores from each debate
    debate_ids = []
    debates_by_year = defaultdict(list)
    debate_x_values = {}

    for debate in debates:
        # Construct the command
        cmd = ['python3', 'readlvl.py', '--year', str(debate['year']), '--candidates'] + debate['candidates'] + ['--colors'] + debate['colors']
        if debate.get('suffix'):
            cmd.extend(['--suffix', debate['suffix']])

        # Run the command and capture the output
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command executed successfully
        if result.returncode != 0:
            print(f"Error running command: {' '.join(cmd)}")
            print(result.stderr)
            continue

        # Extract the output
        output = result.stdout

        # Parse the output to extract the scores
        lines = output.strip().split('\n')
        scores_json = ''
        for i, line in enumerate(lines):
            if line.startswith('Scores for'):
                # The next line should contain the JSON scores
                if i + 1 < len(lines):
                    scores_json = lines[i + 1]
                break

        if not scores_json:
            print(f"Scores not found in output for debate {debate['year']}{debate.get('suffix', '')}")
            continue

        # Parse the JSON string
        try:
            scores_dict = json.loads(scores_json)
        except json.JSONDecodeError as e:
            print(f"Error parsing scores for debate {debate['year']}{debate.get('suffix', '')}: {e}")
            continue

        year = debate['year']
        suffix = debate.get('suffix', '')
        debate_id = f"{year}{suffix}"
        debate_ids.append(debate_id)
        debates_by_year[year].append(debate_id)

        candidates = debate['candidates']
        colors = debate['colors']

        # Create a mapping from color to candidate
        color_candidate_map = dict(zip(colors, candidates))
        color_candidate_map = {color: candidate.upper() for color, candidate in color_candidate_map.items()}

        # Get the candidate names for 'blue' and 'red'
        blue_candidate = color_candidate_map.get('blue')
        red_candidate = color_candidate_map.get('red')

        if not blue_candidate or not red_candidate:
            print(f"Missing blue or red candidate in debate {debate_id}")
            continue

        # Store the scores for each metric
        for metric in metrics:
            metric_scores = scores_dict.get(metric, {})
            blue_score = metric_scores.get(blue_candidate)
            red_score = metric_scores.get(red_candidate)

            if blue_score is not None:
                scores_over_time[metric]['blue'][debate_id] = blue_score
            else:
                print(f"Missing blue score in debate {debate_id}, metric {metric}")
            if red_score is not None:
                scores_over_time[metric]['red'][debate_id] = red_score
            else:
                print(f"Missing red score in debate {debate_id}, metric {metric}")

    # Save the collected scores to a file
    with open(results_filename, 'w') as f:
        json.dump(scores_over_time, f)
    print(f"Results saved to {results_filename}")

# Generate x-values for each debate, adding gaps within the same year
debate_x_values = {}
debate_ids = []
debates_by_year = defaultdict(list)

# Reconstruct debates_by_year and debate_ids from the collected data
for metric in metrics:
    for candidate_color in ['blue', 'red']:
        for debate_id in scores_over_time[metric][candidate_color].keys():
            if debate_id not in debate_ids:
                debate_ids.append(debate_id)
                match = re.match(r'(\d{4})([a-zA-Z]?)', debate_id)
                if match:
                    year = int(match.group(1))
                    debates_by_year[year].append(debate_id)

# Generate x-values
for year in sorted(debates_by_year.keys()):
    debate_ids_in_year = sorted(debates_by_year[year])
    num_debates = len(debate_ids_in_year)
    if num_debates == 1:
        x_positions = [year]
    else:
        # Spread debates within the same year between -0.2 and +0.2
        offsets = np.linspace(-0.7, 0.7, num_debates)
        x_positions = [year + offset for offset in offsets]
    for debate_id, x in zip(debate_ids_in_year, x_positions):
        debate_x_values[debate_id] = x

# Now, get a sorted list of debate_ids based on x_values
debate_ids_sorted = sorted(debate_ids, key=lambda d_id: debate_x_values[d_id])

# Plot the scores over time for each metric
for metric in metrics:
    # Dictionaries to hold x and y values for each candidate
    candidate_data = {
        'blue': {'x': [], 'y': []},
        'red': {'x': [], 'y': []}
    }

    for debate_id in debate_ids_sorted:
        x_value = debate_x_values[debate_id]
        blue_score = scores_over_time[metric]['blue'].get(debate_id)
        red_score = scores_over_time[metric]['red'].get(debate_id)

        if blue_score is not None:
            candidate_data['blue']['x'].append(x_value)
            candidate_data['blue']['y'].append(blue_score)

        if red_score is not None:
            candidate_data['red']['x'].append(x_value)
            candidate_data['red']['y'].append(red_score)

    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot blue candidate
    plt.plot(candidate_data['blue']['x'], candidate_data['blue']['y'], color='blue', marker='o', markersize=4, linestyle='-', linewidth=3, label='Democratic Candidate')

    # Plot red candidate
    plt.plot(candidate_data['red']['x'], candidate_data['red']['y'], color='red', marker='o', markersize=4, linestyle='-', linewidth=3, label='Republican Candidate')

    plt.title(f'{metric.replace("\\n", " ")}', fontsize=20, fontweight='bold')
    plt.xlabel('Year', fontsize=18, fontweight='bold')
    plt.ylabel('Score', fontsize=18, fontweight='bold')
    plt.legend()

    # Create x-ticks at integer years
    all_years = sorted(debates_by_year.keys())
    plt.xticks(ticks=all_years, labels=all_years, rotation=45, fontsize=16)

    score_levels = range(3, 13 ,1)
    plt.yticks(ticks=score_levels, labels=score_levels, fontsize=16)
    
    plt.grid(axis='y', which='major', linestyle='--', alpha=0.7)
    plt.grid(axis='x', which='major', linestyle='--', alpha=0.7)

    plt.text(
        -0.05, -0.175, 
        'Source: Transcripts used with permission from the American Presidency Project https://presidency.ucsb.edu',
        ha='left', va='top', fontsize=6, color='gray', transform=plt.gca().transAxes
    )
    plt.text(
        1, -0.175, 
        'https://github.com/faradayberry/debatecloud',
        ha='right', va='top', fontsize=6, color='gray', transform=plt.gca().transAxes
    )

    plt.tight_layout()
    # Save the plot
    metric_name = metric.replace('\n', '_').replace(' ', '_')
    plt.savefig(f'{metric_name}_over_time.png')
    plt.close()
    print(f"Plot saved for metric {metric.replace('\\n', ' ')}")

# Generate x-values for each debate, adding gaps within the same year
debate_x_values = {}
debate_ids = []
debates_by_year = defaultdict(list)

# Reconstruct debates_by_year and debate_ids from the collected data
for metric in metrics:
    for candidate_color in ['blue', 'red']:
        for debate_id in scores_over_time[metric][candidate_color].keys():
            if debate_id not in debate_ids:
                debate_ids.append(debate_id)
                match = re.match(r'(\d{4})([a-zA-Z]?)', debate_id)
                if match:
                    year = int(match.group(1))
                    debates_by_year[year].append(debate_id)

# Generate y-values (years with small offsets)
for year in sorted(debates_by_year.keys()):
    debate_ids_in_year = sorted(debates_by_year[year])
    num_debates = len(debate_ids_in_year)
    if num_debates == 1:
        y_positions = [year]
    elif num_debates == 2:
        offsets = np.linspace(-0.5, 0.5, num_debates)
        y_positions = [year + offset for offset in offsets] 
    else:
        offsets = np.linspace(-1.1, 1.1, num_debates)
        y_positions = [year + offset for offset in offsets]
    for debate_id, y in zip(debate_ids_in_year, y_positions):
        debate_x_values[debate_id] = y

# Now, get a sorted list of debate_ids based on y_values (years)
debate_ids_sorted = sorted(debate_ids, key=lambda d_id: debate_x_values[d_id])

# Plot the delta scores over time for each metric
for metric in metrics:
    deltas = []
    y_values = []
    colors = []
    
    for debate_id in debate_ids_sorted:
        y_value = debate_x_values[debate_id]
        blue_score = scores_over_time[metric]['blue'].get(debate_id)
        red_score = scores_over_time[metric]['red'].get(debate_id)

        if blue_score is not None and red_score is not None:
            delta = red_score - blue_score  # Red minus Blue
            deltas.append(delta)
            y_values.append(y_value)
            # Set the color: blue for negative delta, red for positive delta
            colors.append('red' if delta > 0 else 'blue')
        else:
            print(f"Missing score(s) for debate {debate_id}, metric {metric}")

    # Plotting the bar chart
    plt.figure(figsize=(10, 8))
    plt.axvline(x=0, color='black', linewidth=0.5)  # Line at delta = 0

    # Bar chart with colors based on delta sign
    plt.barh(y=y_values, width=deltas, color=colors, edgecolor='black', height=1.1)

    delta_levels = range(-4, 5 ,1)
    plt.xticks(ticks=delta_levels, labels=delta_levels, fontsize=16)

    # Add labels for the years on the y-axis
    years = range(1960, 2025, 4)
    plt.yticks(ticks=years, labels=years, fontsize=16)
    
    # Add grid for the y-axis
    plt.grid(axis='y', which='major', linestyle='--', alpha=0.7)
    
    # Title and labels
    plt.title(f'{metric.replace("\\n", " ")}', fontsize=20, fontweight='bold')
    plt.xlabel('Delta', fontsize=18, fontweight='bold')
    plt.ylabel('Year', fontsize=18, fontweight='bold')
    
    # Invert the y-axis so earlier years appear at the top
    plt.gca().invert_yaxis()
    
    plt.text(
        -0.1, -0.1, 
        'Source: Transcripts used with permission from the American Presidency Project https://presidency.ucsb.edu',
        ha='left', va='top', fontsize=7, color='gray', transform=plt.gca().transAxes
    )
    plt.text(
        1, -0.1, 
        'https://github.com/faradayberry/debatecloud',
        ha='right', va='top', fontsize=7, color='gray', transform=plt.gca().transAxes
    )

    # Adjust layout to make it tight
    plt.tight_layout()

    # Save the plot
    metric_name = metric.replace('\n', '_').replace(' ', '_')
    plt.savefig(f'delta_{metric_name}_over_time.png')
    plt.close()
    
    print(f"Delta plot saved for metric {metric.replace('\\n', ' ')}")