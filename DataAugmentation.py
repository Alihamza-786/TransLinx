import os
import librosa
from pydub import AudioSegment
import numpy as np
import soundfile as sf
from natsort import natsorted

def augment_audio(file_path, file_name):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)

    # Pitch Shifting
    y_pitched = librosa.effects.pitch_shift(y, sr=sr, n_steps=1.5)  # Shift by 1.5 semitones
    
    # Time Stretching
    y_stretched = librosa.effects.time_stretch(y, rate=1.2)  # 1.2 is the stretch factor
    
    # Add White Noise
    noise = np.random.randn(len(y))
    y_noisy = y + 0.003 * noise
    
    # Save the augmented files in the same directory
    augmented_files = [
        ('stretched', y_stretched),
        ('pitched', y_pitched),
        ('noisy', y_noisy),
    ]
    
    # Save the augmented versions in the same folder as the original file
    for name, y_aug in augmented_files:
        output_path = os.path.join(os.path.dirname(file_path), f'{file_name}_{name}.wav')
        sf.write(output_path, y_aug, sr)
        print(f"Saved {output_path}")

# Directory containing your subfolders (e.g., 'data3' directory)
input_dir = 'data2'

# Process each subfolder inside the input directory
for subfolder_name in os.listdir(input_dir):
    subfolder_path = os.path.join(input_dir, subfolder_name)
    
    if os.path.isdir(subfolder_path):
        # Get the list of .wav files, sorted using natural sort
        sorted_files = natsorted([f for f in os.listdir(subfolder_path) if f.endswith('.wav') and not f.endswith(('_stretched.wav', '_pitched.wav', '_noisy.wav'))])
        for idx, file_name in enumerate(sorted_files):
            print(f"{idx + 1}: {file_name}")
        
        # Process all .wav files in the subfolder in sorted order
        for idx, file_name in enumerate(sorted_files):
            file_path = os.path.join(subfolder_path, file_name)
            # Use the base file name (without extension) for saving augmented versions
            base_file_name = os.path.splitext(file_name)[0]  # E.g., 'a1', 'have1', ...
            augment_audio(file_path, base_file_name)

print("Augmentation completed.")
