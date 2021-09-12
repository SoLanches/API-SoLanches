import os

from dotenv import load_dotenv

from . rest import app

load_dotenv()

SERVER_HOST = os.getenv('SOLANCHES_HOST')
SERVER_PORT = os.getenv('SOLANCHES_PORT')
SERVER_URL = f"{SERVER_HOST}:{SERVER_PORT}"

print(f"Iniciando servidor em: {SERVER_URL}")
app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
