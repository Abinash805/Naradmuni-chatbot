#!/usr/bin/env python3
"""
Simple Audio-to-Text System
Uses only basic Python libraries and Whisper for reliable transcription
"""

import os
import wave
import numpy as np
import whisper
import tempfile
from werkzeug.utils import secure_filename

class SimpleAudioTranscriber:
    def __init__(self):
        self.model = None
        self.model_name = "base"  # Use base model for speed
        
    def load_model(self):
        """Load Whisper model if not already loaded"""
        if self.model is None:
            print("Loading Whisper model...")
            try:
                self.model = whisper.load_model(self.model_name)
                print("Whisper model loaded successfully")
            except Exception as e:
                print(f"Failed to load Whisper model: {e}")
                return False
        return True
    
    def create_simple_wav(self, audio_data, sample_rate=16000):
        """Create a simple WAV file from audio data"""
        try:
            # Create a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Write WAV file with basic parameters
            with wave.open(temp_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            
            return temp_path
        except Exception as e:
            print(f"Error creating WAV file: {e}")
            return None
    
    def transcribe_audio_data(self, audio_data, filename="audio"):
        """Transcribe audio data to text"""
        try:
            # Load model if needed
            if not self.load_model():
                return "Error: Could not load speech recognition model"
            
            print(f"Processing audio: {len(audio_data)} bytes")
            
            # Create simple WAV file
            temp_path = self.create_simple_wav(audio_data)
            if not temp_path:
                return "Error: Could not create audio file"
            
            print(f"Created temp file: {temp_path}")
            
            try:
                # Transcribe using Whisper
                print("Starting transcription...")
                result = self.model.transcribe(
                    temp_path,
                    language="en",
                    task="transcribe",
                    fp16=False
                )
                
                transcription = result["text"].strip()
                print(f"Transcription result: '{transcription}'")
                
                return transcription if transcription else "No speech detected"
                
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                    print(f"Cleaned up temp file: {temp_path}")
                except:
                    pass
                    
        except Exception as e:
            print(f"Transcription error: {e}")
            return f"Error during transcription: {str(e)}"
    
    def transcribe_file(self, file_path):
        """Transcribe audio from file path"""
        try:
            with open(file_path, 'rb') as f:
                audio_data = f.read()
            return self.transcribe_audio_data(audio_data, os.path.basename(file_path))
        except Exception as e:
            return f"Error reading file: {str(e)}"

# Global instance
transcriber = SimpleAudioTranscriber()

def simple_transcribe_audio(file):
    """Simple transcription function for Flask app"""
    try:
        filename = secure_filename(file.filename)
        print(f"Simple transcription for: {filename}")
        
        # Read audio data
        audio_data = file.read()
        if len(audio_data) == 0:
            return "Error: No audio data received"
        
        # Transcribe using simple method
        return transcriber.transcribe_audio_data(audio_data, filename)
        
    except Exception as e:
        print(f"Simple transcription error: {e}")
        return f"Error: {str(e)}"

# Test function
def test_simple_transcription():
    """Test the simple transcription system"""
    print("🧪 Testing Simple Audio-to-Text System...")
    
    # Test with existing voice_input.wav
    if os.path.exists("voice_input.wav"):
        print("Testing with voice_input.wav...")
        result = transcriber.transcribe_file("voice_input.wav")
        print(f"Result: {result}")
    else:
        print("No voice_input.wav found for testing")
    
    print("✅ Simple transcription system ready!")

if __name__ == "__main__":
    test_simple_transcription() 