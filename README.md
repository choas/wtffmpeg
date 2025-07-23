# wtffmpeg - Natural Language to FFmpeg Translator
wtffmpeg is a command-line tool that uses a local Large Language Model (LLM) to translate plain English descriptions of video and audio tasks into executable ffmpeg commands.

Stop searching through Stack Overflow and documentation for that one specific ffmpeg flag. Just ask for what you want.

**Example:**
```bash
> wtff "convert my_video.avi to mp4 with no sound"

Loading model... (this may take a moment)
Model loaded. Generating command...

--- Generated ffmpeg Command ---
ffmpeg -i my_video.avi -an -c:v libx264 my_video.mp4
------------------------------
Execute this command? [y/N] y

Executing: ffmpeg -i my_video.avi -an -c:v libx264 my_video.mp4

ffmpeg version n6.0 Copyright (c) 2000-2023 the FFmpeg developers
...
```

## Features
- Natural Language Interface: Describe complex ffmpeg operations in plain English.
- Local First: Runs entirely on your local machine. No data is sent to external APIs.
- Interactive Execution: Reviews the generated command before giving you the option to execute it.
- GPU Accelerated: Leverages llama-cpp-python to offload model layers to your GPU for faster inference.
- Customizable: Easily swap out different LLM models or customize the system prompt to improve accuracy for your specific needs.

## Installation
This project uses Python 3.8+ and is packaged with pyproject.toml.

1. Clone the Repository

```bash
git clone https://github.com/scottvr/wtffmpeg.git # Replace with your repo URL
cd wtffmpeg
```

2. Create a Virtual Environment

It is highly recommended to install the packages in a virtual environment.
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install llama-cpp-python with Hardware Acceleration

This is the most critical step. For the best performance, you should install llama-cpp-python with the correct build flags for your hardware before installing the project.

For NVIDIA GPUs (CUDA):
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
```

For Apple Silicon (Metal):
```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
```

For CPU Only (OpenBLAS):
```
pip install llama-cpp-python
```

Refer to the official llama-cpp-python documentation for other hardware configurations (ROCm, CLBlast, etc.) or for installation from prebuilt wheels.

4. Install wtffmpeg

Once llama-cpp-python is installed, you can install the project and its dependencies. This will also create the wtff command alias in your virtual environment.
```bash
pip install .
```

## Configuration
1. Download a Model
   
This tool requires a model in the GGUF format. You can download models from Hugging Face. Good candidates include:

Phi-3-mini-4k-instruct-gguf

Mistral-7B-Instruct-v0.2-GGUF

Download your chosen model and place it in the project directory.

2. Set the Model Path

Open the wtffmpeg.py script and update the MODEL_PATH variable to point to your downloaded model file:

**In wtffmpeg.py**

```python
MODEL_PATH = "./your-model-name.gguf"
```

## Usage
Once installed and configured, you can use the wtff command directly from your terminal.

Basic Usage:
```bash
wtff "your ffmpeg instruction in quotes"
```

**Examples:**
```bash
# Convert a file
wtff "turn presentation.mov into a web-friendly mp4"

# Extract audio
wtff "extract the audio from lecture.mp4 and save it as a high-quality mp3"

# Create a clip
wtff "create a 10-second clip from movie.mkv starting at the 2 minute mark"

# Execute without confirmation
wtff -x "resize video.mp4 to 720p"
```

Disclaimer: This tool uses a Large Language Model to generate commands. While it is designed to be accurate, LLMs can make mistakes or "hallucinate" incorrect commands. Always review the generated command carefully before executing it, especially when working with important files.

