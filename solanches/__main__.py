from urllib.parse import urlparse
from dotenv import load_dotenv
import os
from . rest import app

load_dotenv()

SERVER_URL = f"{os.getenv('SOLANCHES_SERVER_HOST')}:{os.getenv('SOLANCHES_SERVER_PORT')}"

url = urlparse(SERVER_URL)
host, port = url.hostname, url.port
print(f"Iniciando servidor em: {url.geturl()}")
if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
