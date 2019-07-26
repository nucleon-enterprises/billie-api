from whats import Whats
from flask import request 
import json 
import asyncio
import requests
import celery



from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

@celery.task
def zap():
    whats = Whats("chrome", "Whatsapp Bot", headless=False, verbose=True) #Start an instance of whatsapp


@app.route("/test", methods=['POST', 'GET'])
def teste():
    """
    List or create notes.
    """
    zap.delay()
    body = str(request.data.get('text', ''))
    return body


@app.route("/zap", methods=['POST']) 

def whatsappFlow():
    (chat, last_message) = whats.check_new_message()
    if last_message != "":
        data = {body:last_message}
        r = requests.post(url=url)
    await request.json() #Wait the request parsing to JSON
    return request



if __name__ == "__main__":
    app.run(debug=True)

