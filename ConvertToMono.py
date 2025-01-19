#Convert to mono
import os
import librosa
import soundfile as sf

def convert_audio_files(input_dir, output_dir, sr=16000):
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Walk through the input directory
    for subdir, _, files in os.walk(input_dir):
        # Create the corresponding output subdirectory
        rel_path = os.path.relpath(subdir, input_dir)
        output_subdir = os.path.join(output_dir, rel_path)
        
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        
        for file in files:
            if file.lower().endswith('.wav'):
                # Full path to input file
                input_file = os.path.join(subdir, file)
                
                # Load the audio file with librosa
                y, _ = librosa.load(input_file, sr=sr, mono=True)
                
                # Full path to output file
                output_file = os.path.join(output_subdir, file)
                
                # Save the audio file with soundfile
                sf.write(output_file, y, sr)
                
                print(f'Converted {input_file} to {output_file}')

# Define input and output directories
input_directory = 'segmented_test2'
output_directory = 'mono_test_data2'
# Convert audio files
convert_audio_files(input_directory, output_directory)
