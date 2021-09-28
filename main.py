from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json2table
from IPython.core.display import display, HTML

from cryptography.fernet import Fernet

app = FastAPI()

longToShortMappings = {}
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
    return {'long_url': url, 'short_url': getShortUrl(url)}

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
    if long_url not in longToShortMappings:
        short_url = "asianpower.com/" + str(convertLongtoShortUrl(long_url))[-7:]
        longToShortMappings[long_url] = short_url
        shortTolongMappings[short_url] = long_url
    return longToShortMappings[long_url]   

def convertLongtoShortUrl(long_url):
    return fernet.encrypt(long_url.encode())

@app.get('/json')
async def display_():
    return {'mappings': longToShortMappings}

@app.get('/html', response_class=HTMLResponse)
async def display_html():
    infoFromJson = longToShortMappings
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"style": "width:100%"}
    return json2table.convert(infoFromJson, 
                         build_direction=build_direction, 
                         table_attributes=table_attributes)



