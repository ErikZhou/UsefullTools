#!/bin/bash

# First check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Please install Homebrew first:"
        echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    brew install ffmpeg
fi

# Check if input directory is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory_path>"
    echo "Example: $0 ~/Videos"
    exit 1
fi

# Convert all MP4 files in the specified directory
directory="$1"
if [ ! -d "$directory" ]; then
    echo "Directory $directory does not exist!"
    exit 1
fi

echo "Converting MP4 files to MP3 in $directory..."

# Find all MP4 files and convert them
find "$directory" -name "*.mp4" -type f | while read -r file; do
    output_file="${file%.mp4}.mp3"
    echo "Converting: $file"
    ffmpeg -i "$file" -vn -acodec libmp3lame -q:a 2 "$output_file" -hide_banner -loglevel error
done

echo "Conversion complete!"
