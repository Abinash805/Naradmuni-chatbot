#!/usr/bin/env python3
"""
Ultra-Simple Audio-to-Text System
Works directly with audio data in memory - no file operations
"""

import whisper
import numpy as np
import io
import wave
from werkzeug.utils import secure_filename

class UltraSimpleTranscriber:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        """Load Whisper model if not already loaded"""
        if self.model is None:
            print("Loading Whisper model...")
            try:
                self.model = whisper.load_model("base")
                print("Whisper model loaded successfully")
            except Exception as e:
                print(f"Failed to load Whisper model: {e}")
                return False
        return True
    
    def audio_data_to_numpy(self, audio_data):
        """Convert audio data to numpy array"""
        try:
            # Try to read as WAV data
            with io.BytesIO(audio_data) as audio_buffer:
                with wave.open(audio_buffer, 'rb') as wav_file:
                    frames = wav_file.readframes(wav_file.getnframes())
                    audio_array = np.frombuffer(frames, dtype=np.int16)
                    audio_array = audio_array.astype(np.float32) / 32768.0
                    return audio_array
        except Exception as e:
            print(f"Error converting audio data: {e}")
            return None
    
    def transcribe_audio_data(self, audio_data, filename="audio"):
        """Transcribe audio data directly to text"""
        try:
            # Load model if needed
            if not self.load_model():
                return "Error: Could not load speech recognition model"
            
            print(f"Processing audio: {len(audio_data)} bytes")
            
            # Convert audio data to numpy array
            audio_array = self.audio_data_to_numpy(audio_data)
            if audio_array is None:
                return "Error: Could not process audio data"
            
            print(f"Audio converted to numpy array: {len(audio_array)} samples")
            
            # Transcribe using Whisper with numpy array
            print("Starting transcription...")
            result = self.model.transcribe(
                audio_array,
                language="en",
                task="transcribe",
                fp16=False
            )
            
            transcription = result["text"].strip()
            print(f"Transcription result: '{transcription}'")
            
            return transcription if transcription else "No speech detected"
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return f"Error during transcription: {str(e)}"

# Global instance
transcriber = UltraSimpleTranscriber()

def ultra_simple_transcribe_audio(file):
    """Ultra-simple transcription function for Flask app"""
    try:
        filename = secure_filename(file.filename)
        print(f"Ultra-simple transcription for: {filename}")
        
        # Read audio data
        audio_data = file.read()
        if len(audio_data) == 0:
            return "Error: No audio data received"
        
        # Transcribe using ultra-simple method
        return transcriber.transcribe_audio_data(audio_data, filename)
        
    except Exception as e:
        print(f"Ultra-simple transcription error: {e}")
        return f"Error: {str(e)}"

# Test function
def test_ultra_simple_transcription():
    """Test the ultra-simple transcription system"""
    print("🧪 Testing Ultra-Simple Audio-to-Text System...")
    
    # Test with existing voice_input.wav
    if os.path.exists("voice_input.wav"):
        print("Testing with voice_input.wav...")
        with open("voice_input.wav", "rb") as f:
            audio_data = f.read()
        result = transcriber.transcribe_audio_data(audio_data, "voice_input.wav")
        print(f"Result: {result}")
    else:
        print("No voice_input.wav found for testing")
    
    print("✅ Ultra-simple transcription system ready!")

if __name__ == "__main__":
    import os
    test_ultra_simple_transcription() 