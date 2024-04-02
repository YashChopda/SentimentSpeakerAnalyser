FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

# Set the working directory in the container
WORKDIR /app
COPY . /app

# Install system dependencies

RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/m-bain/whisperx.git

# Expose the port the app runs on
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "./app.py"]