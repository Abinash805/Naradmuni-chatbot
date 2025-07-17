#!/usr/bin/env python3
"""
Test script for real speech transcription
"""

import requests
import os

def test_with_real_speech():
    """Test transcription with real speech recording"""
    print("🎤 Testing Real Speech Transcription...")
    print("=" * 50)
    
    # Check if we have a test audio file
    test_files = ["voice_input.wav", "test_speech.wav", "recording.wav"]
    audio_file = None
    
    for file in test_files:
        if os.path.exists(file):
            audio_file = file
            break
    
    if audio_file:
        print(f"✅ Found audio file: {audio_file}")
        
        try:
            # Test the transcription endpoint
            with open(audio_file, "rb") as f:
                files = {"audio": (audio_file, f, "audio/wav")}
                
                print("📤 Sending audio to transcription endpoint...")
                response = requests.post("http://localhost:5000/transcribe", files=files)
                
                print(f"📥 Response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if "transcription" in data:
                        transcription = data["transcription"]
                        print(f"📝 Transcription result: '{transcription}'")
                        
                        if transcription and not transcription.startswith("Voice recording received"):
                            print("🎉 Real speech transcription is working!")
                            return True
                        else:
                            print("⚠️ Transcription returned fallback message")
                            return False
                    else:
                        print("❌ No transcription in response")
                        return False
                else:
                    print(f"❌ Request failed: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    else:
        print("❌ No audio files found for testing")
        print("\n💡 To test with real speech:")
        print("   1. Go to http://localhost:5000 in your browser")
        print("   2. Click 🎤 Start Recording")
        print("   3. Say something like 'What are the engineering courses at GBU'")
        print("   4. Click ⏹️ Stop Recording")
        print("   5. Check if your speech is transcribed correctly")
        return False

def create_test_instructions():
    """Create instructions for testing real speech"""
    print("\n" + "=" * 50)
    print("🎯 HOW TO TEST REAL SPEECH TRANSCRIPTION:")
    print("=" * 50)
    print("1. Open your browser and go to: http://localhost:5000")
    print("2. You'll see the NaradMuni ChatBOT interface")
    print("3. Look for the voice recording controls:")
    print("   - 🎤 Start Recording button")
    print("   - ⏹️ Stop Recording button")
    print("4. Test the voice recording:")
    print("   - Click 🎤 Start Recording")
    print("   - Speak clearly: 'What are the engineering courses at GBU'")
    print("   - Click ⏹️ Stop Recording")
    print("5. Check the result:")
    print("   - If transcription works: You'll see your question in the text box")
    print("   - If it shows fallback message: The system is working but needs optimization")
    print("6. Alternative: Type questions directly in the text box")
    print("\n💡 The text chat works perfectly - you can ask about:")
    print("   - GBU engineering courses")
    print("   - Faculty information")
    print("   - Admission procedures")
    print("   - Campus facilities")
    print("   - And more!")

if __name__ == "__main__":
    print("🚀 Testing Real Speech Transcription System...")
    
    success = test_with_real_speech()
    
    if success:
        print("\n✅ Real speech transcription is working!")
    else:
        print("\n⚠️ Transcription needs testing with real speech")
    
    create_test_instructions() 