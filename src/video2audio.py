import subprocess
import glob
import os

VIDEO_FOLDER = "data/videos/*.mp4"
AUDIO_FOLDER = "data/audio"

def transcribe_video2_audio():
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    video_files = glob.glob(VIDEO_FOLDER)

    if not video_files:
        print("❌ No video files found.")
        return

    for video_file in video_files:
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        audio_file = os.path.join(AUDIO_FOLDER, f"{base_name}.mp3")

        if os.path.exists(audio_file):
            continue

        subprocess.run(
            ["ffmpeg", "-i", video_file, "-q:a", "0", "-map", "a", audio_file],
            check=True
        )
    print("✅ All videos converted to audio.")
