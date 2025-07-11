﻿# Naradmuni Chatbot 🤖

A context-aware chatbot for Gautam Buddha University (GBU) that provides accurate information about university facilities, policies, and resources. The chatbot uses advanced embedding techniques and semantic search to provide relevant answers from the university's documentation.

## Features ✨

- Document Processing:
  - Supports PDF and TXT document formats
  - Smart text chunking for optimal context preservation
  - Automatic document embedding generation
  
- Advanced Search & Response:
  - Semantic search using document embeddings
  - Context-aware responses using relevant document chunks
  - Real-time system resource monitoring (CPU, GPU, Memory)
  
- Persistent Storage:
  - ChromaDB for vector storage
  - Efficient embedding retrieval
  - Automatic embedding updates when documents change

## How It Works 🔍

1. **Document Processing**:
   - Documents in the `data` folder are read and processed
   - Text is extracted and split into manageable chunks
   - Each chunk is converted to embeddings using Nomic Embed Text model

2. **Embedding Storage**:
   - Embeddings are stored in ChromaDB (in the `embeddings` folder)
   - Each embedding represents the semantic meaning of a text chunk
   - Persistent storage ensures quick startup and query response

3. **Query Processing**:
   - User questions are converted to embeddings
   - System finds most relevant document chunks using semantic similarity
   - Context from relevant chunks is used to generate accurate answers
   - System monitors and displays resource usage during processing

## Tech Stack 🛠️

- **Core Technologies**:
  - Flask: Web server and API
  - ChromaDB: Vector database for embeddings
  - Ollama: Model management and inference
  - PyMuPDF (fitz): PDF processing
  
- **Models**:
  - Nomic Embed Text: Document embedding generation
  - Mistral: Response generation
  
- **Monitoring**:
  - NVML: GPU monitoring
  - psutil: System resource monitoring
  - Plotly: Real-time performance graphs

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/Abinash805a/Naradmuni-chatbot.git
cd Naradmuni-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Ollama and pull required models:
```bash
ollama pull nomic-embed-text
ollama pull mistral
```

## Usage 💡

1. Place your documents in the `data` folder (supports .pdf and .txt)

2. Start the Flask server:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

4. Start asking questions about GBU!

## Project Structure 📁

```
demo/
  ├── data/           # Document storage
  │   └── context.txt # University information
  ├── embeddings/     # ChromaDB vector storage
  │   └── ...        # Generated embedding files
  ├── app.py         # Web server and monitoring
  ├── main.py        # Core chatbot logic
  ├── a.py           # Helper functions
  └── requirements.txt
```

## Monitoring Dashboard 📊

The web interface includes a real-time monitoring dashboard that shows:
- CPU Usage
- GPU Usage
- GPU Temperature
- Peak Resource Usage Statistics

This helps track system performance during query processing and ensures optimal resource utilization.
