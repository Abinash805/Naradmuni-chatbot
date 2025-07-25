# Naradmuni Chatbot 🤖

A context-aware chatbot for Gautam Buddha University (GBU) that provides accurate information about university facilities, policies, and resources. The chatbot uses advanced embedding techniques and semantic search to provide relevant answers from the university's documentation.

## Features ✨

- Document Processing:
  - Supports PDF and TXT document formats
  - Smart text chunking for optimal context preservation
  - Automatic document embedding generation
  
- Advanced Search & Response:
  - Semantic search using document embeddings
  - Context-aware responses using relevant document chunks
  
- Persistent Storage:
  - ChromaDB for vector storage
  - Efficient embedding retrieval
  - Automatic embedding updates when documents change

- Audio Support:
  - Voice input via browser (Web Speech API)
  - Audio transcription using OpenAI Whisper (multiple implementations included)

- Web UI & Widget:
  - Modern chat UI (`/chat-ui`)
  - Embeddable widget (`widget.html`) for any website

## How It Works 🔍

1. **Document Processing:**
   - Documents in the `data` folder are read and processed
   - Text is extracted and split into manageable chunks
   - Each chunk is converted to embeddings using Nomic Embed Text model

2. **Embedding Storage:**
   - Embeddings are stored in ChromaDB (in the `embeddings` folder)
   - Each embedding represents the semantic meaning of a text chunk
   - Persistent storage ensures quick startup and query response

3. **Query Processing:**
   - User questions (typed or spoken) are converted to embeddings
   - System finds most relevant document chunks using semantic similarity
   - Context from relevant chunks is used to generate accurate answers

4. **Audio Transcription:**
   - Users can record questions via the chat UI or widget
   - Audio is transcribed using Whisper and processed as a text query

## Tech Stack 🛠️

- **Core Technologies:**
  - Flask: Web server and API
  - ChromaDB: Vector database for embeddings
  - Ollama: Model management and inference
  - PyMuPDF (fitz): PDF processing
  - Whisper: Audio transcription
  
- **Frontend:**
  - HTML/CSS/JS (chat UI, widget)
  - Web Speech API (voice input)

- **Models:**
  - Nomic Embed Text: Document embedding generation
  - Mistral: Response generation

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/Abinash805a/Naradmuni-chatbot.git
cd Naradmuni-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# And install Whisper from GitHub:
pip install git+https://github.com/openai/whisper.git
```

3. Install Ollama and pull required models:
```bash
ollama pull nomic-embed-text
ollama pull mistral
```

4. Install ffmpeg (required for Whisper):
- Download from https://www.gyan.dev/ffmpeg/builds/#release-builds
- Add ffmpeg's bin folder to your system PATH

## Usage 💡

1. Place your documents in the `data` folder (supports .pdf and .txt)

2. Start the Flask server:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000/chat-ui
```

4. To use the widget, open `widget.html` in your browser or embed it in your website. The widget loads the chat UI in an iframe.

5. Use the voice button to record questions, or type them directly.

## Project Structure 📁

```
demo/
  ├── app.py               # Web server and API
  ├── main.py              # Core chatbot logic
  ├── templates/
  │   └── chat-ui.html     # Main chat UI
  ├── widget.html          # Embeddable widget
  ├── data/                # Document storage
  ├── embeddings/          # ChromaDB vector storage
  ├── static/              # Static assets (images, etc.)
  ├── [audio transcriber modules]
  └── requirements.txt
```

## Audio Transcription
- Audio transcription is supported via Whisper.
- Multiple audio transcriber modules are included for flexibility.
- The chat UI and widget both support voice input.

## License
MIT