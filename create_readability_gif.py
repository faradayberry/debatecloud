import imageio
import glob
import re
import os

def get_debate_order(filename):
    """
    Extracts the year and suffix from the filename and returns a tuple for sorting.
    Filenames are expected to be in the format: readability_scores_{year}{suffix}.png
    """
    match = re.match(r'readability_scores_(\d{4})([a-zA-Z]?)\.png', filename)
    if match:
        year = int(match.group(1))
        suffix = match.group(2)
        # Assign numeric values to suffixes for sorting: None -> 0, 'a' -> 1, 'b' -> 2, etc.
        suffix_value = 0
        if suffix:
            suffix_value = ord(suffix.lower()) - ord('a') + 1
        return (year, suffix_value)
    else:
        # If filename doesn't match the expected format, place it at the end
        return (float('inf'), float('inf'))

def create_gif():
    # Get all PNG files starting with 'readability_scores_'
    image_files = glob.glob('readability_scores_*.png')
    if not image_files:
        print("No images found with prefix 'readability_scores_'.")
        return

    # Sort the image files based on year and suffix
    image_files_sorted = sorted(image_files, key=get_debate_order)

    # Read images
    images = []
    for filename in image_files_sorted:
        try:
            image = imageio.imread(filename)
            images.append(image)
            print(f"Added {filename} to GIF.")
        except Exception as e:
            print(f"Could not read {filename}: {e}")

    # Set the frames per second (fps)
    fps = 0.9  # Adjust this value to control the speed of the GIF

    # Save the images as an animated GIF
    output_filename = 'readability_scores_animation.gif'
    imageio.mimsave(output_filename, images, fps=fps, loop=0)
    print(f"Animated GIF saved as {output_filename}")

if __name__ == "__main__":
    create_gif()