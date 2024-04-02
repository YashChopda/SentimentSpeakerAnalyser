# SPEAKER SENTIMENT ANALYSER 

# Text and Audio Processing Web Application

## Overview

This project implements a web application where users can upload text or audio files through a HTML/JavaScript interface. The uploaded files are then processed using Flask, Whisper X for transcription and diarization, and OpenAI API for sentiment analysis. The processed results are then returned to the user via the web interface.

## Features

- **User-friendly Interface**: Provides a simple and intuitive interface for users to upload files.
- **Text and Audio Support**: Supports both text and audio file formats for processing.
- **Automated Processing**: Utilizes Whisper X for transcription and diarization, and OpenAI API for sentiment analysis.
- **Result Visualization**: Displays the processed results back to the user in a clear and understandable format.
- **GPU Acceleration**: Utilizes 1 NVIDIA T4 GPU for faster processing.
- **Dockerized Deployment**: The application is deployed using a Docker image on the Google Cloud Platform (GCP).

## Technologies Used

- **Flask**: Backend server framework for handling file uploads and processing.
- **Whisper X**: Tool for transcription and diarization of audio files.
- **OpenAI API**: API for sending requests to GPT-4 LLM.
- **HTML/JavaScript**: Frontend technologies for building the user interface.
- **Docker**: Containerization technology for packaging the application.
- **Google Cloud Platform (GCP)**: Cloud platform for deployment.
- **NVIDIA T4 GPU**s: GPU hardware for acceleration.

## API Keys Required
- **Github clone** 
- **Huggingface** 
- **OpenAI** 

## Local Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/YashChopda/SentimentSpeakerAnalyser.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    pip install git+https://github.com/m-bain/whisperx.git
    ```

3. Obtain API keys for Whisper X and OpenAI. Place these keys in the appropriate configuration file.

4. Run the Flask application:

    ```bash
    python app.py
    ```
Alternatively, you can choose to build a Docker container using the Dockerfile provided and run it to access the API.

## GCP Deployment

1. The flask server was containerized using Docker.
2. The Docker Image was uploaded to Artifact Registry.
3. A GPU VM instance with CUDA was created.
4. Docker and it's dependencies were installed inside GPU VM instance.
5. The Docker Image was pulled from Artifact Registry.
6. The Docker Image was served via the GPU VM instance.

## Usage

1. Access the web application in your browser. Follow the given steps:
2. Open index.html with any web browser(tested with chrome and safari). An interface will open. ![Web Interface](images/Screenshot%202024-04-02%20at%207.07.42 PM.png)
3. Select and Upload a text or audio file using the provided interface. ![Text/Audio Interface](images/Screenshot%202024-04-02%20at%207.08.06 PM.png)
![Selection of file](images/Screenshot%202024-04-02%20at%207.08.27 PM.png)
4. Wait for the processing to complete. ![Processing](images/Screenshot%202024-04-02%20at%207.08.56 PM.png)
5. View the processed sentiment analysis. ![Result](images/Screenshot%202024-04-02%20at%207.09.08 PM.png)

## Challenges Faced
1. To run it locally I used CPU, which made the processing quite slow, as the model training for first instance took longer.
2. The Instruction and prompt template needed various trials as the output was not consistent each time.
3. During the docker build for ease of deployment, multiple dependency errors especially for WhisperX (like installing ffmpeg) were faced.
4. Deploying the Docker Image on GPU instance was also difficult.

## Acknowledgements

- **Whisper X Team**: For providing the transcription and diarization capabilities.
- **OpenAI Team**: For providing the sentiment analysis API.
- **Google Cloud Platform**: For providing the cloud infrastructure for deployment.

## Contact

For questions or feedback, please contact [yash.chopda7@gmail.com](mailto:yash.chopda7@gmail.com).
