#!/usr/bin/env python3

import argparse
import sys
import subprocess
import shlex
from llama_cpp import Llama

#MODEL_PATH = "./Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf"
#MODEL_PATH='./Phi-3-mini-4k-instruct-q4.gguf'
MODEL_PATH='./mistral-7b-instruct-v0.1.Q3_K_M.gguf'

SYSTEM_PROMPT = """You are an expert at writing commands for the `ffmpeg` multimedia framework.
You will be given a plain-language description of a task.
Your task is to translate this description into a single, complete, and executable `ffmpeg` command.
Respond ONLY with the `ffmpeg` command. Do not add any explanations, introductory text, or markdown formatting.
The command should be on a single line.

Here are some examples:

- User: "convert input.mov to a web-friendly mp4"
- Assistant: ffmpeg -i input.mov -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4

- User: "turn video.avi into an mp4 and remove the audio"
- Assistant: ffmpeg -i video.avi -c:v copy -an output.mp4

- User: "extract the audio from presentation.mp4 and save it as a high-quality mp3"
- Assistant: ffmpeg -i presentation.mp4 -vn -c:a libmp3lame -q:a 0 audio.mp3

- User: "create a 10-second clip from my_movie.mkv starting at the 1 minute 30 second mark"
- Assistant: ffmpeg -i my_movie.mkv -ss 00:01:30 -t 10 -c copy clip.mkv

- User: "extract all frames from between 1 and 5 seconds, and also between 11 and 15 seconds from my_video.avi"
- Assistant: ffmpeg -i my_video.avi -vf select='between(t,1,5)+between(t,11,15)' -vsync 0 out%d.png

- User: "extract 1 frame per second from input.mpg"
- Assistant: ffmpeg -i input.mpg -fps=1 -vsync 0 out%d.png

- User: "convert in.mp4 to avi"
- Assistant: ffmpeg -i in.mp4 out.avi

- User: "remux in.mkv into mp4"
- Assistant: ffmpeg -i in.mkv -c:v copy -c:a copy out.mp4

- User: "make a high-quality conversion of movie.avi as mp4"
- Assistant: ffmpeg -i movie.avi -preset slower -crf 18 out.mp4

- User: "copy the video from in1.mp4 and the audio from in2.mp4 into a new file out12.mp4"
- Assistant: ffmpeg -i in1.mp4 -i in2.mp4 -c copy -map 0:0 -map 1:1 -shortest out12.mp4

- User: "delay the audio of in.mp4 by 3.84 seconds"
- Assistant: ffmpeg -i in.mp4 -itsoffset 3.84 -i in.mp4 -map 0:v -map 1:a -vcodec copy -acodec copy out.mp4

- User: "delay the video of in.mp4 by 6.66 seconds"
- Assistant: ffmpeg -i in.mp4 -itsoffset 6.66 -i in.mp4 -map 1:v -map 0:a -vcodec copy -acodec copy out.mp4

- User: "extract all frames from between 1 and 5 seconds, and also between 11 and 15 seconds from input.mpg"
- Assistant: ffmpeg -i input.mpg -vf select='between(t,1,5)+between(t,11,15)' -vsync 0 out%d.png

- User: "extract one frame per second from starwars.avi"
- Assistant: ffmpeg -i starwars.avi -fps=1 -vsync 0 out%d.png

- User: "rotate in.mov 90 degrees clockwise"
- Assistant: ffmpeg -i in.mov -vf "transpose=1" out.mov

- User: "rotate in.mov 180 degrees"
- Assistant: ffmpeg -i inmov -vf "transpose=2,transpose=2" out.mov

- User: "replace the first 90 seconds of audio in video142.3gp with silence"
- Assistant: ffmpeg -i video142.3gp -vcodec copy -af "volume=enable='lte(t,90)':volume=0" out.mp4

- User: "deinterlace in.mp4. overwrite it."
- Assistant: ffmpeg -i in.mp4 -vf yadif in.mp4 -y

- User: "superimpose the frame number on each frame of movie.mov"
- Assistant: ffmpeg -i movie.mov -vf "drawtext=fontfile=arial.ttf: text=%{n}: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000099: fontsize=72" -y out.mov

- User: "convert input.mkv to mp4"
- Assistant: ffmpeg -i input.mkv -c:a copy -c:v libx264 -crf 17 output.mp4

- User: "create a 24fps video from input*.png"
- Assistant: ffmpeg -framerate 24 -i input*.png output.mp4

- User: "create a new video from seconds 10 through 20 of input.mov"
- Assistant: ffmpeg -ss 10 -i input.mov -t 10 -c copy output.mp4

- User: "reverse the first five seconds of video in input.mp4"
- Assistant: ffmpeg -i input.mp4 -vf trim=end=5,reverse output.mp4

- User: "reverse the first five seconds of audio in input.mp4"
- Assistant: ffmpeg -i input.mp4 -vf trim=end=5,areverse output.mp4

- User: "show me conway's game of life with ffmpeg"
- Assistant: ffmpeg -f lavfi -i life -t 60 output.mp4

- User: "give me a 320x240 smpte bars test pattern of infinite duration"
- Assistant: ffmpeg -f lavfi -i smptebars test_pattern.mp4

- User: "save the audio from concert.mp4 as an mp3"
- Assistant: ffmpeg -i concert.mp4 -vn -c:a libmp3lame -qscale:a 9 concert.mp3

- User: "scale input.mp4 to 1280x720"
- Assistant: ffmpeg -i input.mp4 -vf "scale=1200:720" out.mp4

- User: "add my-watermark.png to my-video.mp4"
- Assistant: ffmpeg -i my-video.mp4 -i my-watermark.png -filter_complex "overlay=36:36" -codec:a copy output.mp4

- User: "set the video bitrate of the my_movie.mov to 64 kbit/s"
- Assistant: ffmpeg -i my_movie.mov -b:v 64k -bufsize 64k output.mp4

- User: "force input.avi to 24 fps. output as webm."
- Assistant: ffmpeg -i input.avi -r 24 output.webm

- User: "write an ID3v2.3 header mp3 file from mysong.flac"
- Assistant: ffmpeg -i mysong.flac -id3v2_version 3 output.mp3

- User: "convert in.avi to mp4; set the title to 'my movie'"
- Assistant: ffmpeg -i in.avi -metadata title="my movie" out.mp4

- User: "make in.mkv's second audio stream the default"
- Assistant: ffmpeg -i in.mkv -c copy -disposition:a:1 default out.mkv

- User: "embed image.png as a thumbnail in mymovie.mp4"
- Assistant: ffmpeg -i mymovie.mp4 -i image.png -map 0 -map 1 -c copy -c:v:1 png -disposition:v:1 attached_pic out.mp4
"""

def generate_ffmpeg_command(prompt: str, llm: Llama) -> str:
    """
    Generates an ffmpeg command by sending a prompt to the LLM.

    Args:
        prompt: The user's natural language request.
        llm: The initialized Llama model instance.

    Returns:
        The generated ffmpeg command as a string.
    """
    try:
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=250
        )
        command = response['choices'][0]['message']['content'].strip()
        
        # Clean up potential model artifacts like prefixes or markdown code blocks.
        if command.lower().startswith("assistant:"):
            command = command[10:].strip()
        if command.startswith("`") and command.endswith("`"):
            command = command.strip("`")

        return command
    except Exception as e:
        print(f"Error during model inference: {e}", file=sys.stderr)
        return ""

def execute_command(command: str):
    """
    Executes a command in the shell and streams its output.

    Args:
        command: The command string to execute.
    """
    print(f"\nExecuting: {command}\n")
    try:
        # Use shlex.split to safely parse the command string
        args = shlex.split(command)
        # Use Popen to run the command and stream output in real-time
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as proc:
            if proc.stdout:
                for line in proc.stdout:
                    print(line, end='')
        
        if proc.returncode == 0:
            print("\n--- Command completed successfully ---")
        else:
            print(f"\n--- Command failed with exit code {proc.returncode} ---", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: The command '{args[0]}' was not found.", file=sys.stderr)
        print("Please ensure ffmpeg is installed and in your system's PATH.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred while trying to execute the command: {e}", file=sys.stderr)


def main():
    """
    Main function to parse arguments, load the model, and run the translation.
    """
    parser = argparse.ArgumentParser(
        description="Translate natural language to an ffmpeg command.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="The natural language instruction for the ffmpeg command.\n"
             "Example: \"convert video.mp4 to audio.mp3\""
    )
    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=-1,
        help="Number of layers to offload to the GPU (-1 for all)."
    )
    parser.add_argument(
        "-x", "--execute",
        action="store_true",
        help="Execute the generated command without confirmation."
    )
    args = parser.parse_args()

    print("Loading model... (this may take a moment)")
    try:
        llm = Llama(
            model_path=MODEL_PATH,
            n_gpu_layers=args.gpu_layers,
            n_ctx=32768,
            verbose=False
        )
    except Exception as e:
        print(f"Error loading model from path: {MODEL_PATH}", file=sys.stderr)
        print(f"Please ensure the MODEL_PATH in the script is correct.", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)
        sys.exit(1)

    print("Model loaded. Generating command...")
    ffmpeg_command = generate_ffmpeg_command(args.prompt, llm)

    if not ffmpeg_command:
        print("Failed to generate a command.", file=sys.stderr)
        sys.exit(1)

    print("\n--- Generated ffmpeg Command ---")
    print(ffmpeg_command)
    print("------------------------------")

    if args.execute:
        execute_command(ffmpeg_command)
    else:
        try:
            # Prompt user for confirmation
            confirm = input("Execute this command? [y/N] ")
            if confirm.lower() == 'y':
                execute_command(ffmpeg_command)
            else:
                print("Execution cancelled by user.")
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+D or Ctrl+C during input
            print("\nExecution cancelled by user.")
            sys.exit(0)


if __name__ == "__main__":
    main()
