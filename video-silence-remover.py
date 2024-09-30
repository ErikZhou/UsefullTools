import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np

def detect_silence(audio_array, threshold=0.01, min_silence_duration=10):
    silent = (np.abs(audio_array).max(axis=1) < threshold)
    silent_ranges = []
    silent_start = None

    for i, is_silent in enumerate(silent):
        if is_silent and silent_start is None:
            silent_start = i
        elif not is_silent and silent_start is not None:
            duration = i - silent_start
            if duration >= min_silence_duration * audio_array.shape[0] / len(silent):
                silent_ranges.append((silent_start / audio_array.shape[0], i / audio_array.shape[0]))
            silent_start = None

    if silent_start is not None:
        duration = len(silent) - silent_start
        if duration >= min_silence_duration * audio_array.shape[0] / len(silent):
            silent_ranges.append((silent_start / audio_array.shape[0], len(silent) / audio_array.shape[0]))

    return silent_ranges

def remove_silence(input_file, output_file, silence_threshold=0.01, min_silence_duration=10):
    try:
        video = VideoFileClip(input_file)
        audio = video.audio

        print(f"Video duration: {video.duration} seconds")
        print(f"Audio duration: {audio.duration} seconds")

        # Try a different method to get audio data
        print("Attempting to read audio data...")
        audio_frames = []
        for t in np.arange(0, audio.duration, 1.0/audio.fps):
            audio_frames.append(audio.get_frame(t))
        audio_array = np.array(audio_frames)
        print(f"Audio array shape: {audio_array.shape}")

        silent_ranges = detect_silence(audio_array, 
                                       threshold=silence_threshold, 
                                       min_silence_duration=min_silence_duration)

        print(f"Detected {len(silent_ranges)} silent ranges")

        if not silent_ranges:
            print("No silent parts found longer than the specified duration.")
            video.write_videofile(output_file)
            return

        clips = []
        last_end = 0

        for start, end in silent_ranges:
            if start > last_end:
                clips.append(video.subclip(last_end, start))
            last_end = end

        if last_end < video.duration:
            clips.append(video.subclip(last_end, video.duration))

        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(output_file)

        video.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove silent parts from a video file.")
    parser.add_argument("input_file", help="Path to the input video file")
    parser.add_argument("output_file", help="Path to the output video file")
    parser.add_argument("--silence_threshold", type=float, default=0.01, 
                        help="Threshold for detecting silence (default: 0.01)")
    parser.add_argument("--min_silence_duration", type=int, default=10, 
                        help="Minimum duration of silence to remove in seconds (default: 10)")

    args = parser.parse_args()

    remove_silence(args.input_file, args.output_file, 
                   args.silence_threshold, args.min_silence_duration)
