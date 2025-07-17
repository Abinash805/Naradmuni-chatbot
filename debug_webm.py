#!/usr/bin/env python3
"""
Debug script for WebM audio processing
"""

import os
import tempfile
import whisper

def debug_webm_audio():
    """Debug WebM audio processing"""
    print("🔍 Debugging WebM Audio Processing...")
    
    # Test with existing voice_input.wav first
    if os.path.exists("voice_input.wav"):
        print("Testing with voice_input.wav...")
        
        # Load Whisper model
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        
        # Test direct transcription
        try:
            print("Trying direct transcription...")
            result = model.transcribe("voice_input.wav")
            print(f"Direct result: '{result['text']}'")
        except Exception as e:
            print(f"Direct transcription failed: {e}")
        
        # Test with temp file
        try:
            print("Trying with temp file...")
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                with open("voice_input.wav", "rb") as source:
                    temp_file.write(source.read())
                temp_path = temp_file.name
            
            print(f"Created temp file: {temp_path}")
            result = model.transcribe(temp_path)
            print(f"Temp file result: '{result['text']}'")
            
            # Clean up
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"Temp file transcription failed: {e}")
    
    print("\n💡 To test with real WebM audio:")
    print("1. Go to http://localhost:5000")
    print("2. Record some speech using the voice button")
    print("3. Check the server logs for detailed error messages")
    print("4. The WebM format from browsers should work with the new code")

if __name__ == "__main__":
    debug_webm_audio() 