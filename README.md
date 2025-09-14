# wtffmpeg - Natural Language to FFmpeg Translator

`wtffmpeg` is a command-line tool that uses a Large Language Model (LLM) to translate plain English descriptions of video and audio tasks into executable `ffmpeg` commands. It can use local models via Ollama or other OpenAI-compatible APIs, as well as the official OpenAI API.

Stop searching through Stack Overflow and documentation for that one specific `ffmpeg` flag. Just ask for what you want.

**Example:**
```bash
> wtff "convert test_pattern.mp4 to a gif file"

INFO: No API key or LLM_API_URL env var provided. Defaulting to local Ollama at http://localhost:11434
--- Generated ffmpeg Command ---
ffmpeg -i test_pattern.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" output.gif
------------------------------
Execute? [y/N], or (c)opy to clipboard: y

Executing: ffmpeg -i test_pattern.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" output.gif

ffmpeg version n7.0 Copyright (c) 2000-2024 the FFmpeg developers
...
```

## Features
- **Natural Language Interface**: Describe complex `ffmpeg` operations in plain English.
- **Flexible LLM Backend**:
    - **Local First**: Connects to local LLMs like Ollama by default.
    - **Cloud Support**: Easily switch to the OpenAI API or other services using an API key or bearer token.
- **Interactive Execution**: Reviews the generated command before giving you the option to execute it.
- **Clipboard Integration**: Copy commands to your clipboard with a single keypress.
- **Interactive Mode**: Run multiple commands in a persistent session.

## Installation

This script uses `uv` to manage its dependencies.

1.  **Install `uv`**:
    If you don't have `uv` installed, you can install it with:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.cargo/env" 
    ```

2.  **Clone and Run**:
    The script is designed to be run directly from the cloned repository. `uv` will automatically create a virtual environment and install the required dependencies (`openai` and `pyperclip`) on the first run.
    ```bash
    git clone https://github.com/scottvr/wtffmpeg.git
    cd wtffmpeg
    chmod +x wtffmpeg.py
    ./wtffmpeg.py "your first prompt"
    ```

3.  **Create an Alias (Optional)**:
    For easier access, you can create a symbolic link to the script in a directory that is in your system's `PATH`.
    ```bash
    sudo ln -s "$(pwd)/wtffmpeg.py" /usr/local/bin/wtff
    ```
    Now you can run the tool from anywhere by simply typing `wtff`.

## Configuration

`wtffmpeg` can be configured using command-line arguments or environment variables.

### Environment Variables

You can create a `.env` file in the project directory or export these variables in your shell. An `example.env` file is provided.

-   `LLM_API_URL`: The base URL for your local LLM API (e.g., `http://localhost:11434`). This is the default connection method if no API key is provided.
-   `OPENAI_API_KEY`: Your API key for the OpenAI service.
-   `BEARER_TOKEN`: A bearer token for authentication with other OpenAI-compatible services.

### Connection Logic

The tool decides which service to use based on the following priority:
1.  If `--api-key` or `OPENAI_API_KEY` is provided, it will connect to the official OpenAI API.
2.  If not, it will look for `--bearer-token` or `BEARER_TOKEN` to authenticate with a custom API endpoint.
3.  If neither of the above is present, it will fall back to using the `--url` or `LLM_API_URL`, defaulting to a local Ollama instance at `http://localhost:11434`.

## Usage

### Command-Line Arguments

```
usage: wtffmpeg.py [-h] [--model MODEL] [--api-key API_KEY] [--bearer-token BEARER_TOKEN] [--url URL] [-x] [-c] [-i] [prompt]

Translate natural language to an ffmpeg command.

positional arguments:
  prompt                The natural language instruction for the ffmpeg command. Required unless running in interactive mode.

options:
  -h, --help            show this help message and exit
  --model MODEL         The model to use. For Ollama, this should be a model you have downloaded. Defaults to 'llama3'.
  --api-key API_KEY     OpenAI API key. Defaults to OPENAI_API_KEY environment variable.
  --bearer-token BEARER_TOKEN
                        Bearer token for authentication. Defaults to BEARER_TOKEN environment variable.
  --url URL             Base URL for a local LLM API (e.g., http://localhost:11434). Defaults to LLM_API_URL env var, then http://localhost:11434. The '/v1' suffix for OpenAI compatibility will be added automatically.
  -x, --execute         Execute the generated command without confirmation.
  -c, --copy            Copy the generated command to the clipboard.
  -i, --interactive     Enter interactive mode to run multiple commands.
```

### Examples

**Using the Default Local Ollama Instance:**
```bash
# The tool defaults to http://localhost:11434 and the 'llama3' model
wtff "turn presentation.mov into a web-friendly mp4"

# Specify a different local model
wtff --model "codellama:7b" "extract the audio from lecture.mp4"
```

**Using the OpenAI API:**
```bash
# The tool will automatically switch to 'gpt-4o' as the default model
export OPENAI_API_KEY="sk-..."
wtff "create a 10-second clip from movie.mkv starting at the 2 minute mark"

# Or provide the key as an argument
wtff --api-key "sk-..." "resize video.mp4 to 720p"
```

**Interactive Mode:**
```bash
# Start an interactive session with a specific model
wtff --model "gemma:2b" -i
```

Inside interactive mode, you can type `!` followed by a shell command to execute it directly. This is useful for listing files (`!ls -l`) or making quick edits.

## Disclaimer

This was largely made to amuse myself; consider it a piece of humorous performance art but it so borders on being actually useful, I went to the trouble to document all of this. YMMV. Use at your own risk. The author is not responsible for any damage or data loss that may occur from using this tool. Always review generated commands before executing them, especially when working with important files.