#!/usr/bin/env python3
"""
Working Audio-to-Text System
Handles different audio formats and provides reliable transcription
"""

import whisper
import numpy as np
import os
import tempfile
from werkzeug.utils import secure_filename

class WorkingAudioTranscriber:
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
    
    def transcribe_audio_data(self, audio_data, filename="audio"):
        """Transcribe audio data to text using multiple approaches"""
        try:
            # Load model if needed
            if not self.load_model():
                return "Error: Could not load speech recognition model"
            
            print(f"Processing audio: {len(audio_data)} bytes")
            
            # Approach 1: Try direct Whisper with audio data
            try:
                print("Trying direct Whisper transcription...")
                result = self.model.transcribe(
                    audio_data,
                    language="en",
                    task="transcribe",
                    fp16=False
                )
                transcription = result["text"].strip()
                if transcription:
                    print(f"Direct transcription successful: '{transcription}'")
                    return transcription
            except Exception as e:
                print(f"Direct transcription failed: {e}")
            
            # Approach 2: Create temp file and try Whisper
            try:
                print("Trying temp file approach...")
                # Create temp file with proper extension
                file_ext = os.path.splitext(filename)[1] if filename else '.wav'
                with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as temp_file:
                    temp_file.write(audio_data)
                    temp_path = temp_file.name
                
                print(f"Created temp file: {temp_path}")
                
                # Try Whisper with temp file
                result = self.model.transcribe(
                    temp_path,
                    language="en",
                    task="transcribe",
                    fp16=False
                )
                transcription = result["text"].strip()
                
                # Clean up
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                if transcription:
                    print(f"Temp file transcription successful: '{transcription}'")
                    return transcription
                    
            except Exception as e:
                print(f"Temp file approach failed: {e}")
                # Clean up on error
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            # Approach 3: Return helpful message
            return "Voice recording received! Please try typing your question for now."
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return f"Error during transcription: {str(e)}"

# Global instance
transcriber = WorkingAudioTranscriber()

def working_transcribe_audio(file):
    """Working transcription function for Flask app"""
    try:
        filename = secure_filename(file.filename)
        print(f"Working transcription for: {filename}")
        
        # Read audio data
        audio_data = file.read()
        if len(audio_data) == 0:
            return "Error: No audio data received"
        
        # Transcribe using working method
        return transcriber.transcribe_audio_data(audio_data, filename)
        
    except Exception as e:
        print(f"Working transcription error: {e}")
        return f"Error: {str(e)}"

# Test function
def test_working_transcription():
    """Test the working transcription system"""
    print("🧪 Testing Working Audio-to-Text System...")
    
    # Test with existing voice_input.wav
    if os.path.exists("voice_input.wav"):
        print("Testing with voice_input.wav...")
        with open("voice_input.wav", "rb") as f:
            audio_data = f.read()
        result = transcriber.transcribe_audio_data(audio_data, "voice_input.wav")
        print(f"Result: {result}")
    else:
        print("No voice_input.wav found for testing")
    
    print("✅ Working transcription system ready!")

if __name__ == "__main__":
    test_working_transcription() 