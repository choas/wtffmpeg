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

ffmpeg version N-100029-g040e989223 Copyright (c) 2000-2020 the FFmpeg developers
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
git clone https://github.com/scottvr/wtffmpeg.git
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

(Note: the default model file is Phi-3-mini-4k-instruct-q4.gguf, but you can override this with the --model option when running wtff.)
)
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

# Specify a different LLM and start interactive mode
wtff --model mistral-7b-instruct-v0.1.Q3_K_M.gguf -i
```

## Troubleshooting

Sometimes the model may generate commands that are not valid ffmpeg syntax or otherwise do not work as expected. In this example, I'll work in interactive mode, but the same principles apply in one-off mode.

```bash
$ wtff -i
...
Model loaded.
Entering interactive mode. Type 'exit' or 'quit' to leave.
wtff> reverse the video test_pattern.mp4
--- Generated ffmpeg Command ---
ffmpeg -i test_pattern.mp4 -vf "reverse" -c copy output.mp4
------------------------------
Execute? [y/N], or (c)opy to clipboard: N
```

Here the model incorrectly added the `-c copy` flag, which is not valid when using a filter like `-vf "reverse"`, and had we executed this command, ffmpeg would have given us an explicit error telling us that the `-c copy` flag is not compatible with the filter. 

So while we *could* copy the commmand to our clipboard, and execute it with the `! command` syntax from within interactive mode after pasting and editing the command-line,let's edit our wtff prompt to ensure that the model does not add the `-c copy` flag in this case. We'll just up-arrow to get our prompt history and add a sentence to our prompt:

```bash
wtff> reverse the video test_pattern.mp4. Do not use `-c copy` in your command.

--- Generated ffmpeg Command ---
ffmpeg -i test_pattern.mp4 -vf "reverse" -c:v libx264 -crf 18 -pix_fmt yuv420p output.mp4
------------------------------
Execute? [y/N], or (c)opy to clipboard: 
```

That command will work just fine so we can either allow wtff to execute it, or we can copy it to our clipboard and execute it manually with `! command` syntax.

The `!command` syntax is a feature of wtffmpeg that allows you to execute any command from within the wtff interactive mode. This is useful if you want to run a command that was generated by the model but needs some manual adjustments, or if you want to run a completely different command without leaving the interactive session. Like this:

```bash
Model loaded.
Entering interactive mode. Type 'exit' or 'quit' to leave.
wtff> !ls -l *.mp4

Executing: ls -l *.mp4

-rwxrwxrwx 1 scottvr scottvr 249093 Jul 22 21:30 output.mp4
-rwxrwxrwx 1 scottvr scottvr 243716 Jul 22 19:45 test_pattern.mp4

--- Command completed successfully ---
wtff>
```

So of course if you want to stay in interaactive mode, you can have it copy the commands to your clipboard, type `!` and paste the contents of your clipboard, and then hit enter to execute the command, without having to leave that terminal, reload the model, etc.

# Disclaimer

This was largely made to amuse myself; consider it a piece of humorous performance art but it so borders on being actually useful, I went to the trouble to document all of this. YMMV. Use at your own risk. The author is not responsible for any damage or data loss that may occur from using this tool. Always review generated commands before executing them, especially when working with important files.
