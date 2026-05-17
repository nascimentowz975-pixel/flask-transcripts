from flask import Flask, send_from_directory, request
import os

app = Flask(__name__)

TRANSCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transcripts')
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

UPLOAD_SECRET = os.environ.get("UPLOAD_SECRET", "tiradentes123")

@app.route('/upload', methods=['POST'])
def upload():
    secret = request.headers.get('X-Secret')
    if secret != UPLOAD_SECRET:
        return "Não autorizado", 401

    file = request.files.get('file')
    if not file:
        print("Nenhum arquivo recebido!")
        print("Files:", request.files)
        print("Data:", request.data)
        return "Nenhum arquivo enviado", 400

    filepath = os.path.join(TRANSCRIPTS_DIR, file.filename)
    file.save(filepath)
    print(f"Arquivo salvo: {file.filename}")
    return "OK", 200

@app.route('/transcripts/<path:filename>')
def transcript(filename):
    filepath = os.path.join(TRANSCRIPTS_DIR, filename)
    if not os.path.exists(filepath):
        return f"Arquivo não encontrado: {filename}", 404
    return send_from_directory(TRANSCRIPTS_DIR, filename)

@app.route('/listar')
def listar():
    arquivos = os.listdir(TRANSCRIPTS_DIR)
    return {"arquivos": arquivos}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
