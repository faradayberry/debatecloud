import argparse
import matplotlib.pyplot as plt
import textstat
from collections import defaultdict
import numpy as np
import json

def load_transcript(file_path):
    with open(file_path, 'r') as file:
        transcript = file.read()
    return transcript

def parse_transcript(transcript, candidate_names):
    speakers = defaultdict(str)
    lines = transcript.splitlines()
    current_speaker = None

    for line in lines:
        # Strip whitespace from the line
        line = line.strip()
        # Skip empty lines
        if not line:
            continue

        # Check if the line starts with "MODERATOR:"
        if line.startswith("MODERATOR:"):
            current_speaker = None  # Reset current speaker
            continue  # Ignore this line and subsequent lines until a candidate speaks

        # Check if the line starts with any candidate's name
        speaker_found = False
        for candidate in candidate_names:
            candidate_tag = f"{candidate.upper()}:"
            if line.startswith(candidate_tag):
                current_speaker = candidate.upper()
                # Remove the candidate's name from the line
                line = line.replace(candidate_tag, "").strip()
                speaker_found = True
                break

        if not speaker_found:
            if current_speaker:
                # Line is a continuation of the current speaker's speech
                pass
            else:
                # No current speaker, ignore the line
                continue

        # Append the line to the current speaker's text
        if current_speaker:
            speakers[current_speaker] += " " + line

    return speakers

def calculate_readability(speakers_text):
    readability_scores = defaultdict(dict)

    for speaker, text in speakers_text.items():
        fk_grade = textstat.flesch_kincaid_grade(text)
        fog_index = textstat.gunning_fog(text)
        smog_index = textstat.smog_index(text)
        coleman_liau_index = textstat.coleman_liau_index(text)
        
        readability_scores['Flesch-Kincaid Grade Level'][speaker] = fk_grade
        readability_scores['Gunning Fog Index'][speaker] = fog_index
        readability_scores['Simple Measure of Gobbledygook'][speaker] = smog_index
        readability_scores['Coleman-Liau Index'][speaker] = coleman_liau_index

    return readability_scores

def plot_readability(readability_scores, candidate_names, candidate_colors, output_file):
    # Metric names without newlines
    metrics = list(readability_scores.keys())

    # Metric labels with newlines for plotting
    metric_labels = {
        'Flesch-Kincaid Grade Level': 'Flesch-Kincaid\nGrade Level',
        'Gunning Fog Index': 'Gunning Fog\nIndex',
        'Simple Measure of Gobbledygook': 'Simple Measure\nof Gobbledygook',
        'Coleman-Liau Index': 'Coleman-Liau\nIndex'
    }

    # Use labels with newlines for x-tick labels
    metric_labels_list = [metric_labels[metric] for metric in metrics]

    # Force the speakers to follow the order of `candidate_names`
    speakers = [candidate.upper() for candidate in candidate_names]
    num_candidates = len(speakers)

    bar_width = 0.9 / num_candidates
    total_group_width = bar_width * num_candidates
    index = np.arange(len(metrics))
        
    plt.figure(figsize=(10, 6))
    
    speaker_colors = {candidate.upper(): color for candidate, color in zip(candidate_names, candidate_colors)}
    
    for i, speaker in enumerate(speakers):
        scores = [readability_scores[metric][speaker] for metric in metrics]
        
        # Calculate positions for each bar
        positions = index - (total_group_width / 2) + (i * bar_width) + bar_width
        
        bars = plt.bar(
            positions, 
            scores, 
            bar_width, 
            label=speaker, 
            color=speaker_colors[speaker]
        )
        
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2, 
                height - 0.5, 
                f'{height:.2f}', 
                ha='center', 
                va='bottom', 
                fontsize=11, 
                fontweight='bold', 
                color='white'
            )
    
    plt.ylabel('Reading Level', fontweight='bold', fontsize=14)
    suffix_title = args.suffix.upper() if args.suffix else ""
    plt.title(f'US Presidential Debate {args.year}{suffix_title} Reading Levels', fontweight='bold', fontsize=16)
    plt.ylim(0, 12)
    plt.xticks([x + (bar_width / 2) for x in index], metric_labels_list, fontweight='bold', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.text(
        -0.05, -0.1, 
        'Source: Transcripts used with permission from the American Presidency Project https://presidency.ucsb.edu',
        ha='left', va='top', fontsize=6, color='gray', transform=plt.gca().transAxes
    )
    plt.text(
        1, -0.1, 
        'https://github.com/faradayberry/debatecloud',
        ha='right', va='top', fontsize=6, color='gray', transform=plt.gca().transAxes
    )

    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze readability scores for debate candidates.")
    parser.add_argument('--year', type=int, required=True, help='The year of the debate (e.g., 2024)')
    parser.add_argument('--suffix', type=str, help='The optional suffix for the debate (e.g., a, b, c)')
    parser.add_argument('--candidates', nargs='+', required=True, help='The names of the candidates (e.g., Trump Harris)')
    parser.add_argument('--colors', nargs='+', required=True, help='The colors for the candidates (e.g., red blue)')
    
    args = parser.parse_args()
    
    if len(args.candidates) != len(args.colors):
        raise ValueError("The number of candidates must match the number of colors provided.")
    
    # Construct the file path using the year, and optionally the suffix if provided
    suffix = args.suffix.lower() if args.suffix else ""
    file_path = f'transcript{args.year}{suffix}.txt'
    
    transcript = load_transcript(file_path)
    
    candidates = [name.strip() for name in args.candidates]
    colors = [color.strip() for color in args.colors]
    
    speakers_text = parse_transcript(transcript, candidates)
    readability_scores = calculate_readability(speakers_text)
    
    # Construct the output file name using the year and optional suffix
    output_file = f'readability_scores_{args.year}{suffix}.png'
    
    plot_readability(readability_scores, candidates, colors, output_file)
    print(f"Plot saved as {output_file}")

    # Convert the readability_scores defaultdict to a regular dict
    readability_scores_dict = {k: dict(v) for k, v in readability_scores.items()}

    # Serialize to JSON
    readability_scores_json = json.dumps(readability_scores_dict)

    # Include the suffix in the year if available
    suffix_display = f".{args.suffix.lower()}" if args.suffix else ""

    # Print the scores
    print(f"Scores for {args.year}{suffix_display}:")
    print(readability_scores_json)