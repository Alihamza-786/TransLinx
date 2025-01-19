#Make Segments
import subprocess
import os
from pydub import AudioSegment, silence

def convert_m4a_to_wav(input_file, wav_file):
    """Converts M4A to WAV using ffmpeg."""
    command = [
        'ffmpeg',
        '-i', input_file,
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        wav_file
    ]
    subprocess.run(command, check=True)

def load_audio(input_file):
    """Loads the audio file into an AudioSegment object, converting if necessary."""
    file_ext = os.path.splitext(input_file)[-1].lower()

    if file_ext == '.m4a':
        # Convert M4A to WAV
        wav_file = 'temp_audio.wav'
        convert_m4a_to_wav(input_file, wav_file)
        audio = AudioSegment.from_wav(wav_file)
        return audio, wav_file  # Return the temp wav file path to delete later
    elif file_ext == '.wav':
        # Directly load WAV file
        audio = AudioSegment.from_wav(input_file)
        return audio, None  # No temp file created
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

def split_audio(input_file, output_folder, min_silence_len=300, silence_thresh=-30, keep_silence=300, padding_duration=500):
    """
    Splits the audio into chunks based on silence, ensures complete words are retained, and adds padding.
    
    Parameters:
    - input_file: Path to the input M4A or WAV file.
    - output_folder: Directory where the segmented WAV files will be saved.
    - min_silence_len: Minimum length of silence to be used for a split (in ms).
    - silence_thresh: Silence threshold in dBFS. Adjusted to be less sensitive.
    - keep_silence: Amount of silence to leave at the beginning and end of each chunk (in ms).
    - padding_duration: Duration of silence padding added before and after each chunk (in ms).
    """
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the audio (converts M4A to WAV if necessary)
    audio, temp_wav_file = load_audio(input_file)
    
    try:
        # Detect non-silent chunks with adjusted parameters
        chunks = silence.split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            keep_silence=keep_silence
        )
        
        # Add silence padding
        padding = AudioSegment.silent(duration=padding_duration)  # Silence padding
        
        # Optionally limit the number of segments
        num_segments = min(len(chunks), 20)
        
        for i, chunk in enumerate(chunks[:num_segments]):
            # Add padding before and after the chunk
            padded_chunk = padding + chunk + padding
            
            # Define the output file path
            output_file = os.path.join(
                output_folder, 
                f'{os.path.splitext(os.path.basename(input_file))[0]}{i + 1}.wav'
            )
            # Export the chunk
            padded_chunk.export(output_file, format='wav')
            print(f'Saved {output_file}')
    
    finally:
        # Remove the temporary WAV file if created
        if temp_wav_file:
            os.remove(temp_wav_file)

def process_all_files(input_folder, output_folder_base, min_silence_len=300, silence_thresh=-30, keep_silence=300, padding_duration=500):
    """
    Processes all M4A and WAV files in the input folder and splits them into segments with padding.
    
    Parameters:
    - input_folder: Directory containing the input M4A and WAV files.
    - output_folder_base: Base directory where all segmented folders will be created.
    - min_silence_len: Minimum length of silence to be used for a split (in ms).
    - silence_thresh: Silence threshold in dBFS.
    - keep_silence: Amount of silence to keep around each chunk (in ms).
    - padding_duration: Duration of silence padding added to each chunk (in ms).
    """
    # Ensure the base output directory exists
    os.makedirs(output_folder_base, exist_ok=True)
    
    # Iterate over all files in the input folder
    for file_name in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file_name)
        
        if os.path.isfile(input_file) and file_name.lower().endswith(('.m4a', '.wav')):
            base_name = os.path.splitext(file_name)[0]
            output_folder = os.path.join(output_folder_base, base_name)
            
            # Process the file
            split_audio(
                input_file, 
                output_folder, 
                min_silence_len=min_silence_len, 
                silence_thresh=silence_thresh, 
                keep_silence=keep_silence,
                padding_duration=padding_duration
            )

# Usage
input_folder = 'test'
output_folder_base = 'segmented_test2'

process_all_files(input_folder, output_folder_base)

