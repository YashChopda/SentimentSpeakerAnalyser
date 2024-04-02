# Import necessary libraries
from openai import OpenAI
import os
import whisperx
import json
import gc
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import torch

# Template for instructions to be provided in the prompt
INSTRUCT_TEMPLATE = """
Assume you are a Hiring Manager. Your task is to take in a transcript of an interview and then provide a psychological analysis of the speakers.
For each speaker you need to provide psychological/sentimental insights that you can extract from the conversation. Remember to be professional and give insights for each speaker in a different line. 
There can be more than 2 speakers, so give the output accordingly and include all the speakers who are mentioned in the transcript.
You should output strictly in the following JSON format:
{
  "[Speaker_1]" : "their analysis..",
  "[Speaker_2]" : "their analysis..",
  ...
  "[Speaker_n]" : "their analysis..",
  
}
"""

# Template for the prompt to be passed to OpenAI chat completions
PROMPT_TEMPLATE = """
Here is the transcript: [TRANSCRIPT]
"""

# OpenAI API Key
OPEN_AI_KEY = "YOUR_OPEN_AI_API KEY"
os.environ["OPENAI_API_KEY"] = OPEN_AI_KEY

# Hugging Face token
HF_TOKEN = "YOUR HUGGING FACE TOKEN"

# OpenAI Model
OPENAI_MODEL = "gpt-4-1106-preview"

# Function to read text file
def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.read()
            return lines
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to get response from OpenAI based on transcript
def get_response(transcript):
    response_prompt = PROMPT_TEMPLATE + ""
    response_prompt = response_prompt.replace("[TRANSCRIPT]", transcript)
    client = OpenAI()
    print(response_prompt)
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": INSTRUCT_TEMPLATE},
            {"role": "user", "content": response_prompt}
        ]
    )
    output = completion.choices[0].message.content.strip()
    output_json = json.loads(output)
    print(output_json)
    return output_json

# Function to load WhisperX model
def get_whisperx_model(device="cpu", batch_size=8, compute_type="int8", model_type="tiny"):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device)
    model = whisperx.load_model(model_type, device, compute_type=compute_type)
    return model

# Function to transcribe audio
def transcribe_audio(model, audio_file, batch_size=8, device="cpu"):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    print(result["segments"])
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    return result

# Function to diarize audio
def diarize_audio(audio_file, result, device="cpu"):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    audio = whisperx.load_audio(audio_file)
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=device)
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    return diarize_segments

# Function to transcribe audio and get speakers
def transcribe_and_get_speakers(audio_file, model):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    result = transcribe_audio(model, audio_file)
    diarize_segments = diarize_audio(audio_file, result)
    transcript_str = ""
    for segment in result["segments"]:
        transcript_str += str(segment["speaker"]) + ": "
        transcript_str += segment["text"]
        transcript_str += "\n "
    return transcript_str

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Define upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load WhisperX model
model = get_whisperx_model()

# API endpoint to perform query
@app.route('/api/query', methods=['POST'])
def perform_query():
    if request.method == 'POST':
        query = request.json
        transcript = query['transcript']
        response = get_response(transcript)
        output_json = {'response': response}
        return jsonify(output_json)

# API endpoint to perform text query
@app.route('/api/text/query', methods=['POST'])
def perform_text_query():
    file = request.files.get('file')
    if file and file.filename.endswith('.txt'):
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        transcript_lines = read_txt_file(filename)
        response = get_response(transcript_lines)
        output_json = {'response': response}
        return jsonify(output_json)

# API endpoint to perform audio query
@app.route('/api/audio/query', methods=['POST'])
def perform_audio_query():
    file = request.files.get('file')
    if file and file.filename.endswith('.mp3'):
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        transcript_lines = transcribe_and_get_speakers(filename, model)
        response = get_response(transcript_lines)
        output_json = {'response': response}
        return jsonify(output_json)

# Run the Flask app
app.run(host='0.0.0.0', port=5000)
