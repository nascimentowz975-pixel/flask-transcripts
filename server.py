from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Pasta transcripts dentro do próprio app
TRANSCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transcripts')

@app.route('/transcripts/<path:filename>')
def transcript(filename):
    filepath = os.path.join(TRANSCRIPTS_DIR, filename)
    if not os.path.exists(filepath):
        return f"Arquivo não encontrado: {filename}", 404
    return send_from_directory(TRANSCRIPTS_DIR, filename)

@app.route('/listar')
def listar():
    if not os.path.exists(TRANSCRIPTS_DIR):
        return "Pasta transcripts não existe!", 500
    arquivos = os.listdir(TRANSCRIPTS_DIR)
    return {"arquivos": arquivos}

if __name__ == '__main__':
    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)