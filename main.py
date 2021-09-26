from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import re

from cryptography.fernet import Fernet

app = FastAPI()

urlMappings = {}
shortTolongMappings = {}

key = Fernet.generate_key()
fernet = Fernet(key)

key = Fernet.generate_key()
fernet = Fernet(key)

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def render(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.post('/shortener')
def read_url(url: str = Form(...)):
    url = url.replace("https://www.","")
    url = url.replace("www.","")
    return {'long_url': url, 'encrypted': getShortUrl(url),
        'mappings': urlMappings}

@app.post('/redirect')
async def redirect_fastapi(url2: str = Form(...), q: Optional[str] = None):
    if (shortUrlExists(url2)):
        long_url = shortTolongMappings[url2]
        if "https" not in long_url:
            long_url = "https://" + long_url +"/"
        return RedirectResponse(long_url)
    

def getLongUrl(short_url):
    if short_url in shortTolongMappings:
        return shortTolongMappings[short_url]
    return None

def shortUrlExists(short_url):
    return short_url in shortTolongMappings.keys()

def getShortUrl(long_url):
    if long_url not in urlMappings:
        short_url = "asianpower.com/" + str(convertLongtoShortUrl(long_url))[-7:]
        urlMappings[long_url] = short_url
        shortTolongMappings[short_url] = long_url
    return urlMappings[long_url]   

def convertLongtoShortUrl(long_url):
    return fernet.encrypt(long_url.encode())

