from pydub import AudioSegment
import os

print("Current directory:", os.getcwd())
print("File exists:", os.path.exists("voice_input.wav"))

try:
    audio = AudioSegment.from_file("voice_input.wav", format="wav")
    print("Loaded audio length (ms):", len(audio))
    print("Channels:", audio.channels)
    print("Frame rate:", audio.frame_rate)
    print("Sample width:", audio.sample_width)
except Exception as e:
    print("❌ Error loading audio with pydub:", e)

# Try ffmpeg directly
import subprocess
try:
    result = subprocess.run(["ffmpeg", "-i", "voice_input.wav"], capture_output=True, text=True)
    print("ffmpeg output:")
    print(result.stdout)
    print(result.stderr)
except Exception as e:
    print("❌ Error running ffmpeg:", e) 