import matplotlib.pyplot as plt
import textstat
from collections import defaultdict

def load_transcript(file_path):
    with open(file_path, 'r') as file:
        transcript = file.read()
    return transcript

def parse_transcript(transcript):
    speakers = defaultdict(str)
    
    lines = transcript.splitlines()
    current_speaker = None
    
    for line in lines:
        if line.startswith("TRUMP:"):
            current_speaker = "TRUMP"
            line = line.replace("TRUMP:", "").strip()
        elif line.startswith("HARRIS:"):
            current_speaker = "HARRIS"
            line = line.replace("HARRIS:", "").strip()
        elif line.startswith("MUIR:") or line.startswith("DAVIS:"):
            current_speaker = None 
            
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
        
        readability_scores['Flesch-Kincaid\nGrade Level'][speaker] = fk_grade
        readability_scores['Gunning Fog\nIndex'][speaker] = fog_index
        readability_scores['Simple Measure\nof Gobbledygook'][speaker] = smog_index
        readability_scores['Coleman-Liau\nIndex'][speaker] = coleman_liau_index

    return readability_scores

def plot_readability(readability_scores, output_file):
    metrics = list(readability_scores.keys())
    speakers = list(next(iter(readability_scores.values())).keys())
    
    bar_width = 0.35
    index = range(len(metrics))
    
    plt.figure(figsize=(10, 6))
    
    speaker_colors = {
        'TRUMP': 'red',
        'HARRIS': 'blue'
    }
    
    for i, speaker in enumerate(speakers):
        scores = [readability_scores[metric][speaker] for metric in metrics]
        bars = plt.bar([x + i * bar_width for x in index], scores, bar_width, 
                       label=speaker, color=speaker_colors[speaker])
        
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2, height - 0.5, f'{height:.2f}', 
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='white'
            )
    
    plt.ylabel('Reading Level', fontweight='bold', fontsize=14)
    plt.title('US Presidential Debate Sept. \'24 Reading Levels', fontweight='bold', fontsize=16)
    plt.xticks([x + (bar_width / 2) for x in index], metrics, fontweight='bold', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()

if __name__ == "__main__":
    file_path = 'transcript.txt'
    transcript = load_transcript(file_path)
    speakers_text = parse_transcript(transcript)
    readability_scores = calculate_readability(speakers_text)
    output_file = 'readability_scores.png'
    plot_readability(readability_scores, output_file)
    print(f"Plot saved as {output_file}")