import os
import json
import whisper
import argparse
import logging
from pathlib import Path
from tqdm import tqdm
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def find_media_files(directory, extensions={'.mp3', '.wav', '.mp4', '.mkv', '.flac'}):
    """Recursively scans a directory for media files with specified extensions."""
    media_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                media_files.append(os.path.join(root, file))
    return media_files

def format_timestamp(seconds):
    """Converts seconds to SRT timestamp format (HH:MM:SS,MS)."""
    millisec = int((seconds % 1) * 1000)
    time_obj = str(timedelta(seconds=int(seconds))).zfill(8)  # Ensures HH:MM:SS format
    return f"{time_obj},{millisec:03d}"

def generate_subtitles(file_path, model):
    """Transcribes the given media file and formats the output as subtitles."""
    try:
        result = model.transcribe(file_path, word_timestamps=True)
        segments = result.get('segments', [])
        
        srt_content = ""
        for idx, segment in enumerate(segments, start=1):
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            text = segment['text']
            srt_content += f"{idx}\n{start_time} --> {end_time}\n{text}\n\n"

        return result['text'], srt_content

    except Exception as e:
        logging.error(f"Error transcribing {file_path}: {e}")
        return None, None

def save_transcription(file_path, text, srt_text, output_dir):
    """Saves the transcription as .txt, .json, and .srt files."""
    base_name = Path(file_path).stem
    output_text_path = os.path.join(output_dir, f"{base_name}.txt")
    output_json_path = os.path.join(output_dir, f"{base_name}.json")
    output_srt_path = os.path.join(output_dir, f"{base_name}.srt")

    try:
        # Save as plain text
        with open(output_text_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        # Save as JSON
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump({"file": file_path, "transcription": text}, json_file, ensure_ascii=False, indent=4)

        # Save as SRT
        with open(output_srt_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_text)

        logging.info(f"Saved transcription: {output_text_path}, {output_json_path}, {output_srt_path}")

    except Exception as e:
        logging.error(f"Error saving transcription for {file_path}: {e}")

def process_file(media_file, model, output_folder):
    """Processes a single media file: transcribes and saves subtitles."""
    transcription, srt_text = generate_subtitles(media_file, model)
    if transcription:
        save_transcription(media_file, transcription, srt_text, output_folder)

def main(input_folder, output_folder):
    """Main function to process media files in the input folder."""
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the highest accuracy model available
    logging.info("Loading Whisper large-v3 model for maximum accuracy...")
    model = whisper.load_model("large-v3")

    media_files = find_media_files(input_folder)
    logging.info(f"Found {len(media_files)} media files.")

    with ThreadPoolExecutor(max_workers=4) as executor:  # Process 4 files in parallel
        list(tqdm(executor.map(lambda f: process_file(f, model, output_folder), media_files), total=len(media_files), desc="Generating Subtitles"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", type=str, help="Path to the input folder containing media files")
    parser.add_argument("output_folder", type=str, help="Path to the output folder to save transcriptions")

    args = parser.parse_args()

    main(args.input_folder, args.output_folder)
