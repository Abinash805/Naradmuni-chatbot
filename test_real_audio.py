#!/usr/bin/env python3
"""
Test script to verify real audio transcription is working
"""

import os
import sys
from main import transcribe_audio
from werkzeug.datastructures import FileStorage

def test_with_real_audio(audio_file_path):
    """Test transcription with a real audio file"""
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
        return
    
    print(f"🧪 Testing with real audio file: {audio_file_path}")
    
    try:
        # Create a FileStorage object from the real audio file
        with open(audio_file_path, 'rb') as f:
            file_storage = FileStorage(
                stream=f,
                filename=os.path.basename(audio_file_path),
                content_type="audio/wav"  # Adjust based on your file type
            )
            
            # Test transcription
            result = transcribe_audio(file_storage)
            print(f"📝 Transcription result: '{result}'")
            
            if result and result != "Error: Could not process audio file. Please try again or use text input.":
                if result == "No speech detected":
                    print("⚠️ No speech detected - this might be normal for silence or noise")
                else:
                    print("✅ Real audio transcription is working!")
            else:
                print("❌ Audio transcription failed")
                
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

def test_with_voice_input():
    """Test with the voice_input.wav file if it exists"""
    voice_file = "voice_input.wav"
    if os.path.exists(voice_file):
        print(f"🎤 Found voice input file: {voice_file}")
        test_with_real_audio(voice_file)
    else:
        print(f"❌ No voice input file found: {voice_file}")
        print("💡 To test with real audio:")
        print("   1. Record some speech and save as 'voice_input.wav'")
        print("   2. Run this script again")
        print("   3. Or provide a different audio file path as argument")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test with provided audio file
        test_with_real_audio(sys.argv[1])
    else:
        # Test with voice_input.wav if it exists
        test_with_voice_input() 