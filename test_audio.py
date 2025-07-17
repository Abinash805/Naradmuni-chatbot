#!/usr/bin/env python3
"""
Test script to verify audio transcription is working properly
"""

import os
import tempfile
import wave
import numpy as np
from main import transcribe_audio
from werkzeug.datastructures import FileStorage

def create_test_audio():
    """Create a simple test WAV file with a sine wave"""
    # Create a simple sine wave audio
    sample_rate = 16000
    duration = 2  # seconds
    frequency = 440  # Hz (A note)
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create temporary WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        with wave.open(temp_file.name, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        return temp_file.name

def test_transcription():
    """Test the transcription function"""
    print("🧪 Testing audio transcription...")
    
    # Create test audio file
    test_audio_path = create_test_audio()
    print(f"Created test audio file: {test_audio_path}")
    
    try:
        # Create a mock FileStorage object
        with open(test_audio_path, 'rb') as f:
            file_storage = FileStorage(
                stream=f,
                filename="test_audio.wav",
                content_type="audio/wav"
            )
            
            # Test transcription
            result = transcribe_audio(file_storage)
            print(f"📝 Transcription result: '{result}'")
            
            if result and result != "Error: Could not process audio file. Please try again or use text input.":
                print("✅ Audio transcription is working!")
            else:
                print("❌ Audio transcription failed")
                
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    
    finally:
        # Clean up test file
        try:
            os.unlink(test_audio_path)
            print(f"🧹 Cleaned up test file: {test_audio_path}")
        except:
            pass

if __name__ == "__main__":
    test_transcription() 