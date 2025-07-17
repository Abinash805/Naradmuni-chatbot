from flask import Flask, request, jsonify
from flask_cors import CORS
from main import answer_query, transcribe_audio, main as setup_embeddings
import threading
import os
import psutil
import time
from collections import deque
import json
import pynvml  # For NVIDIA GPU monitoring
from flask import render_template
from collections import Counter

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for development

# Initialize embeddings in a separate thread
print("Setting up embeddings...")
threading.Thread(target=setup_embeddings).start()

# Initialize NVML
try:
    pynvml.nvmlInit()
    print("NVML initialized successfully")
except Exception as e:
    print(f"Failed to initialize NVML: {e}")

# Store baseline and historical stats
baseline_stats = None
stats_history = deque(maxlen=30)  # Store 30 seconds of data
query_in_progress = False
peak_stats = {
    'cpu': 0,
    'memory': 0,
    'gpu_load': 0,
    'gpu_memory': 0,
    'gpu_temp': 0,
    'gpu_temp_actual': 0
}

FAQ_LOG_FILE = "faq_log.json"
def log_question(question):
    if not question.strip():
        return

    try:
        if os.path.exists(FAQ_LOG_FILE):
            with open(FAQ_LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = {}

        logs[question] = logs.get(question, 0) + 1

        with open(FAQ_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        print(f"Error logging question: {e}")
        
def get_gpu_stats():
    """Get GPU statistics using NVML."""
    gpu_stats = []
    try:
        deviceCount = pynvml.nvmlDeviceGetCount()
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            
            # Get device name - handle both bytes and str return types
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            
            # Get utilization rates
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_util = utilization.gpu
            
            # Get memory info
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            memory_used = memory_info.used / (1024 * 1024)  # Convert to MB
            memory_total = memory_info.total / (1024 * 1024)  # Convert to MB
            
            # Get temperature with better error handling
            try:
                temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            except (pynvml.NVMLError, Exception) as e:
                print(f"Error getting GPU temperature: {e}")
                temperature = 0
            
            gpu_stats.append({
                'name': name,
                'load': gpu_util,
                'memory_used': round(memory_used, 2),
                'memory_total': round(memory_total, 2),
                'temperature': temperature
            })
            
            # Update peak stats if query is in progress
            if query_in_progress:
                peak_stats['gpu_temp'] = max(peak_stats['gpu_temp'], temperature)
                peak_stats['gpu_temp_actual'] = max(peak_stats['gpu_temp_actual'], temperature)
    except Exception as e:
        print(f"Error getting GPU stats: {e}")
    
    return gpu_stats

def update_peak_stats(cpu_percent, memory_percent, gpu_stats):
    """Update peak statistics during monitoring."""
    if not query_in_progress or not gpu_stats:
        return
        
    peak_stats['cpu'] = max(peak_stats['cpu'], cpu_percent)
    peak_stats['memory'] = max(peak_stats['memory'], memory_percent)
    peak_stats['gpu_load'] = max(peak_stats['gpu_load'], gpu_stats[0]['load'])
    peak_stats['gpu_memory'] = max(peak_stats['gpu_memory'], gpu_stats[0]['memory_used'])
    peak_stats['gpu_temp'] = max(peak_stats['gpu_temp'], gpu_stats[0]['temperature'])
    peak_stats['gpu_temp_actual'] = max(peak_stats['gpu_temp_actual'], gpu_stats[0]['temperature'])

def get_system_stats():
    """Get system statistics including CPU, memory, and GPU."""
    try:
        # CPU and memory stats
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 * 1024 * 1024)  # Convert to GB
        memory_total = memory.total / (1024 * 1024 * 1024)  # Convert to GB
        
        # GPU stats
        gpu_stats = get_gpu_stats()
        
        stats = {
            'cpu_percent': round(cpu_percent, 2),
            'memory_used': round(memory_used, 2),
            'memory_total': round(memory_total, 2),
            'memory_percent': round(memory.percent, 2),
            'gpu_stats': gpu_stats,
            'timestamp': time.time()
        }

        # Calculate relative changes if baseline exists and we have GPU stats
        if baseline_stats and gpu_stats:
            stats['relative'] = {
                'gpu': [{
                    'load': round(gpu_stats[i]['load'] - baseline_stats['gpu_stats'][i]['load'], 2),
                    'memory': round(gpu_stats[i]['memory_used'] - baseline_stats['gpu_stats'][i]['memory_used'], 2),
                    'temp': round(gpu_stats[i]['temperature'] - baseline_stats['gpu_stats'][i]['temperature'], 2)
                } for i in range(len(gpu_stats))]
            }
            
            # Update peak stats
            update_peak_stats(cpu_percent, memory.percent, gpu_stats)

        # Add to history
        stats_history.append(stats)
        return stats
    except Exception as e:
        print(f"Error getting system stats: {str(e)}")
        return None

def reset_peak_stats():
    """Reset peak statistics to initial values."""
    global peak_stats
    peak_stats = {
        'cpu': 0,
        'memory': 0,
        'gpu_load': 0,
        'gpu_memory': 0,
        'gpu_temp': 0,
        'gpu_temp_actual': 0
    }

@app.route('/chat-ui')
def chat_ui():
    return render_template('chat-ui.html')

@app.route('/start-monitoring', methods=['POST'])
def start_monitoring():
    global baseline_stats, query_in_progress
    baseline_stats = get_system_stats()
    query_in_progress = True
    reset_peak_stats()
    return jsonify({'status': 'success'})

@app.route('/stop-monitoring', methods=['POST'])
def stop_monitoring():
    global query_in_progress
    query_in_progress = False
    return jsonify({'status': 'success', 'peak_stats': peak_stats})

@app.route('/system-stats')
def system_stats():
    stats = get_system_stats()
    if stats:
        return jsonify(stats)
    return jsonify({'error': 'Failed to get system stats'}), 500

@app.route('/stats-history')
def get_stats_history():
    return jsonify(list(stats_history))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        question = data['question']
        log_question(question)
        
        answer = answer_query(data['question'])
        return jsonify({
            'answer': answer,
            'peak_stats': peak_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    text = transcribe_audio(audio_file)
    return jsonify({'transcription': text})

@app.route('/top-faqs', methods=['GET'])
def top_faqs():
    try:
        if not os.path.exists(FAQ_LOG_FILE):
            return jsonify([])

        with open(FAQ_LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)

        sorted_faqs = sorted(logs.items(), key=lambda x: x[1], reverse=True)
        top_n = [q for q, _ in sorted_faqs[:5]]  # top 5 questions
        return jsonify(top_n)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 