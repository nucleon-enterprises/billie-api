from fastapi import FastAPI
from whats import Whats
from flask import request 
import json 
import asyncio
import requests
url='localhost'
app = FastAPI() #Start an instance of FastAPI
whats = Whats("firefox", "Whatsapp Bot", headless=False, verbose=True) #Start an instance of whatsapp

@app.route("/zap", methods=['POST'])
async def 

def whatsappFlow(request):
    (chat, last_message) = whats.check_new_message()
    if last_message != "":
        data = {body:last_message}
        r = request.post(url=url)
    request.json() #Wait the request parsing to JSON
    return request


while True:


whats.close()