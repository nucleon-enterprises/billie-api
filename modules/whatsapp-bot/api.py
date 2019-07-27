from whats import Whats
from flask import Flask
import json 
from multiprocessing import Process
import requests
from flask import request, url_for
whats = Whats("chrome", "Whatsapp Bot", headless=False, verbose=True)

def sendMessageToCore(msg):
    pass

def zap(whats):
    while True:
        (chat, last_message) = whats.check_new_message()
        if last_message != "" and last_message[0]=='/': #If the new message is a command,
            sendMessageToCore(last_message)             #send it to core   

zapThread = Process(target=zap, args=([whats])) 
zapThread.start()
 
homePage='''kkk eae men
'''


app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    return homePage


@app.route("/test", methods=['POST'])
def teste():

    body = str(request.form.get('body'))
    print('kk eae men  '+body)
    return homePage

if __name__ == "__main__":
    app.run(debug=True)

