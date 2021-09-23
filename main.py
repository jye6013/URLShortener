from typing import Optional
from fastapi import FastAPI
from cryptography.fernet import Fernet

app = FastAPI()

urlMappings = {}

key = Fernet.generate_key()
fernet = Fernet(key)

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/item/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
    return {'item_id': item_id, "q": q}

@app.get('/shortener/{long_url}')
def read_url(long_url: str):
    return {'long_url': long_url, 'encrypted': getShortUrl(long_url), 
    'decrypted': fernet.decrypt(urlMappings[long_url]).decode()}

def getShortUrl(long_url):
    if (not(long_url in urlMappings)):
        urlMappings[long_url] = convertLongtoShortUrl(long_url)
    return urlMappings[long_url]

def convertLongtoShortUrl(long_url):
    return fernet.encrypt(long_url.encode())

