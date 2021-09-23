from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from cryptography.fernet import Fernet

app = FastAPI()

urlMappings = {}

key = Fernet.generate_key()
fernet = Fernet(key)

key = Fernet.generate_key()
fernet = Fernet(key)

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def render(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/shortener')
def read_url(long_url: str = Form(...)):
    print(long_url)
    # return url
    return {'long_url': long_url, 'encrypted': getShortUrl(long_url), 
    'decrypted': fernet.decrypt(urlMappings[long_url]).decode()}



