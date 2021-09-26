from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import re

from cryptography.fernet import Fernet

app = FastAPI()

longtoShortMappings = {}
shortTolongMappings = {}

key = Fernet.generate_key()
fernet = Fernet(key)

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def render(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.post('/shortener')
def read_url(url: str = Form(...)):
    url = url.replace("https://www.","")
    url = url.replace("http://www.","")
    url = url.replace("https://","")
    url = url.replace("http://","")
    url = url.replace("www.","")
    return {'long_url': url, 'short_url': getShortUrl(url),
        'mappings': longtoShortMappings}

@app.post('/redirect')
async def redirect_fastapi(url2: str = Form(...), q: Optional[str] = None):
    if (shortUrlExists(url2)):
        long_url = shortTolongMappings[url2]
        if "https" not in long_url:
            long_url = "https://www." + long_url + "/"
        return RedirectResponse(long_url)
    
def shortUrlExists(short_url):
    return short_url in shortTolongMappings.keys()

def getShortUrl(long_url):
    if long_url not in longtoShortMappings:
        short_url = "asianpower.com/" + str(convertLongtoShortUrl(long_url))[-7:]
        longtoShortMappings[long_url] = short_url
        shortTolongMappings[short_url] = long_url
    return longtoShortMappings[long_url]   

def convertLongtoShortUrl(long_url):
    return fernet.encrypt(long_url.encode())

