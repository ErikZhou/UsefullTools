from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np

def remove_silence(input_file, output_file, silence_threshold=-50.0, min_silence_duration=10):
    video = VideoFileClip(input_file)
    audio = video.audio

    # Process audio in chunks
    chunk_size = 1000  # 1 second chunks
    silent_ranges = []
    current_silent_start = None

    for i in range(0, int(audio.duration * 1000), chunk_size):
        start = i / 1000.0
        end = min((i + chunk_size) / 1000.0, audio.duration)
        chunk = audio.subclip(start, end)
        
        # Get max volume of the chunk
        chunk_array = chunk.to_soundarray()
        max_volume = np.abs(chunk_array).max()

        is_silent = max_volume < (10 ** (silence_threshold / 20))

        if is_silent and current_silent_start is None:
            current_silent_start = start
        elif not is_silent and current_silent_start is not None:
            if start - current_silent_start >= min_silence_duration:
                silent_ranges.append((current_silent_start, start))
            current_silent_start = None

    # Check if the last chunk was silent
    if current_silent_start is not None and audio.duration - current_silent_start >= min_silence_duration:
        silent_ranges.append((current_silent_start, audio.duration))

    # Create non-silent clips
    non_silent_clips = []
    last_end = 0

    for start, end in silent_ranges:
        if start > last_end:
            non_silent_clips.append(video.subclip(last_end, start))
        last_end = end

    if last_end < video.duration:
        non_silent_clips.append(video.subclip(last_end, video.duration))

    # Concatenate non-silent clips
    if non_silent_clips:
        final_clip = concatenate_videoclips(non_silent_clips)
        final_clip.write_videofile(output_file, codec="libx264")
    else:
        print("No non-silent parts found. The entire video is silent.")

    video.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Remove silence from a video file.")
    parser.add_argument("input_file", help="Path to the input video file.")
    parser.add_argument("output_file", help="Path to the output video file.")
    parser.add_argument("--silence_threshold", type=float, default=-50.0, 
                        help="Threshold for detecting silence in dB (default: -50.0)")
    parser.add_argument("--min_silence_duration", type=float, default=10.0, 
                        help="Minimum duration of silence to remove in seconds (default: 10.0)")
    args = parser.parse_args()

    remove_silence(args.input_file, args.output_file, 
                   silence_threshold=args.silence_threshold, 
                   min_silence_duration=args.min_silence_duration)
