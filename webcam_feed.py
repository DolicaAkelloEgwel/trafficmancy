import subprocess

# Live stream URL
YOUTUBE_URL = "https://www.youtube.com/watch?v=jzgnL2FkrXc"

# Output filename
OUTPUT_FILE = "latest.mp4"

# yt-dlp command to grab the latest 10 seconds of a live stream
command = [
    "yt-dlp",
    "--download-sections",
    "*-10",  # Download the most recent 10 seconds
    "-o",
    OUTPUT_FILE,  # Output file name
    YOUTUBE_URL,
]

# Run command
subprocess.run(command)

print(f"Downloaded latest 10s clip: {OUTPUT_FILE}")
