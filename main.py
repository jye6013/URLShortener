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
def read_url(url: str = Form(...)):

    # short url    
    if (shortUrlExists(url)):
        print("short url exists")
    else:
        return {'long_url': url, 'encrypted': getShortUrl(url),
         'mappings': urlMappings}



def getLongUrl(short_url):
    for key, value in urlMappings.iteritems():
        if value == short_url:
            return key

def shortUrlExists(short_url):
    if short_url in urlMappings.values():
        return True
    else:
        return False

def getShortUrl(long_url):
    if long_url not in urlMappings:
        urlMappings[long_url] = "asianpower.com/" + str(convertLongtoShortUrl(long_url))[-7:]
    return urlMappings[long_url]   

def convertLongtoShortUrl(long_url):
    return fernet.encrypt(long_url.encode())

