#!/usr/bin/env python3
"""
Test script to verify voice recording and transcription endpoint
"""

import requests
import os

def test_transcription_endpoint():
    """Test the /transcribe endpoint with a real audio file"""
    print("🧪 Testing voice recording and transcription endpoint...")
    
    # Check if voice_input.wav exists
    if not os.path.exists("voice_input.wav"):
        print("❌ No voice_input.wav file found")
        print("💡 To test voice recording:")
        print("   1. Go to http://localhost:5000 in your browser")
        print("   2. Click the 🎤 Start Recording button")
        print("   3. Speak your question")
        print("   4. Click ⏹️ Stop Recording")
        return
    
    print(f"✅ Found voice input file: voice_input.wav")
    
    try:
        # Test the /transcribe endpoint
        with open("voice_input.wav", "rb") as audio_file:
            files = {"audio": ("voice_input.wav", audio_file, "audio/wav")}
            
            print("📤 Sending audio to /transcribe endpoint...")
            response = requests.post("http://localhost:5000/transcribe", files=files)
            
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if "transcription" in data:
                    transcription = data["transcription"]
                    print(f"✅ Transcription successful: '{transcription}'")
                    
                    if transcription and not transcription.startswith("Error"):
                        print("🎉 Voice recording and transcription is working!")
                    else:
                        print("⚠️ Transcription returned an error message")
                else:
                    print("❌ No transcription in response")
                    print(f"Response: {data}")
            else:
                print(f"❌ Request failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

def test_chat_endpoint():
    """Test the /chat endpoint with a text question"""
    print("\n🧪 Testing chat endpoint...")
    
    try:
        question = "What are the engineering courses at GBU?"
        print(f"📤 Sending question: '{question}'")
        
        response = requests.post("http://localhost:5000/chat", 
                               json={"question": question})
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "answer" in data:
                answer = data["answer"]
                print(f"✅ Chat response: '{answer[:100]}...'")
                print("🎉 Chat functionality is working!")
            else:
                print("❌ No answer in response")
                print(f"Response: {data}")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    print("🚀 Testing NaradMuni ChatBOT Voice Recording...")
    print("=" * 50)
    
    test_transcription_endpoint()
    test_chat_endpoint()
    
    print("\n" + "=" * 50)
    print("🎯 To use the voice recording feature:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Click 🎤 Start Recording")
    print("   3. Speak your question about GBU")
    print("   4. Click ⏹️ Stop Recording")
    print("   5. Your question will be transcribed and answered automatically!")
    print("\n💡 You can also type questions directly in the text box.") 