from flask import Flask, request, jsonify, render_template, send_file
from kokoro import KPipeline
import soundfile as sf
import json
import os
from datetime import datetime
import threading

app = Flask(__name__)

with open('data.json', 'r') as f:
    VOICE_OPTIONS = json.load(f)

pipeline = KPipeline(lang_code='a')

@app.route('/')
def index():
    return render_template('index.html', voices=VOICE_OPTIONS)

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    text = request.form.get('text', '')
    voice = request.form.get('voice', 'af_alloy')
    speed = float(request.form.get('speed', 1))
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S_%f")[:-3]
    output_filename = f'static/audio/{timestamp}.wav'
    
    os.makedirs('static/audio', exist_ok=True)
    
    try:
        generator = pipeline(
            text, 
            voice=voice,
            speed=speed, 
            split_pattern=r'\n+'
        )
        
        gs, ps, audio = next(generator)
        
        sf.write(output_filename, audio, 24000)
        
        return jsonify({
            "success": True,
            "audioUrl": f"/static/audio/{timestamp}.wav",
            "filename": f"{timestamp}.wav"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'static/audio/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)