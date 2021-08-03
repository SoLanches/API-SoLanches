from urllib.parse import urlparse

from . rest import app


SERVER_URL = "http://0.0.0.0:5000"

url = urlparse(SERVER_URL)
host, port = url.hostname, url.port
print(f"Iniciando servidor em: {url.geturl()}")
app.run(host=host, port=port, debug=True)
