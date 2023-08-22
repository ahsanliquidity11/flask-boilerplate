import requests
import json

import os
import openai
import tempfile
import math
import subprocess
from flask import Flask, request, jsonify
from datetime import datetime

openai.api_key = "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"

app = Flask(__name__)

def convert_meet_recording_to_audio(input_file, output_file):
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_file,
                "-vn",
                "-acodec",
                "libmp3lame",
                "-q:a",
                "2",
                output_file,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Conversion successful!")
    except subprocess.CalledProcessError as e:
        print("FFmpeg error output:", e.stderr)
        raise

def transcribe_audio(file_path):
    file_size = os.path.getsize(file_path)
    file_size_in_mb = file_size / (1024 * 1024)
    if file_size_in_mb < 25:
        with open(file_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language='en'
            )
            transcription_text = response.text
        return transcription_text
    else:
        print("Please provide a smaller audio file (max 25mb).")

def divide_segments(file_path, segment_size_mb):
    file_size = os.path.getsize(file_path)
    num_segments = math.ceil(file_size / (segment_size_mb * 1024 * 1024))

    transcripts = []

    with open(file_path, "rb") as audio_file:
        for i in range(num_segments):
            segment_start = i * segment_size_mb * 1024 * 1024
            segment_end = min((i + 1) * segment_size_mb * 1024 * 1024, file_size)
            segment_data = audio_file.read(segment_end - segment_start)

            segment_filename = f"segment_{i}.wav"
            with open(segment_filename, "wb") as segment_file:
                segment_file.write(segment_data)

            transcript = transcribe_audio(segment_filename)
            transcripts.append(transcript)

            os.remove(segment_filename)

    return transcripts

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio_endpoint():
    data = request.json
    file_path = data.get("file_path")
    
         # Generate a unique output file name based on date and time
    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d_%H%M%S")
    output_file = f"output_{date_time_str}.mp3"

    # Convert the meeting recording to audio
    convert_meet_recording_to_audio(file_path, output_file)

    # Divide the audio into segments and transcribe them
    transcripts = divide_segments(output_file, segment_size_mb=24)

    return jsonify(transcripts)

if __name__ == '__main__':
   app.run()
