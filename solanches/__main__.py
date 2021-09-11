from urllib.parse import urlparse
import os

from . rest import app


SERVER_HOST = os.getenv('SOLANCHES_HOST')
SERVER_PORT = os.getenv('SOLANCHES_PORT')
SERVER_URL = f"{SERVER_HOST}:{SERVER_PORT}"

url = urlparse(SERVER_URL)
host, port = url.hostname, url.port
print(f"Iniciando servidor em: {url.geturl()}")
app.run(host=host, port=port, debug=True)
