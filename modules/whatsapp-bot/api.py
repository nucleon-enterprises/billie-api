from whats import Whats
from flask import Flask
import json 
from multiprocessing import Process
import requests
from flask import request, url_for
import os
from getsystem import getsys


whats = Whats("chrome", "Whatsapp Bot", headless=False, verbose=True)

def sendMessageToCore(msg, type):
    r = requests.post('http://localhost:5000/billie', data={'body': msg, 'type':type})


def zap(whats):
    while True:
        (chat, last_message) = whats.check_new_message()
        if str(last_message) != '':
            sendMessageToCore(last_message, '')
        #send it to core   

            if last_message[0]=='/': #If the new message is a command,
                sendMessageToCore(last_message[1:], 'command')

zapThread = Process(target=zap, args=([whats])) 
zapThread.start()
 
homePage='''kkk eae men
'''

app = Flask(__name__)


@app.route("/", methods=['GET'])
def root():
    return homePage

@app.route("/billie", methods=['POST'])
def billie():

    body = str(request.form.get('body'))
    type = str(request.form.get('type'))
    if type =='command':
        commandOutput = os.popen(body).read()
        whats.send_message(commandOutput, 'Whatsapp Bot')
    if type == 'response':
        whats.send_message(body, 'Whatsapp Bot')
    return homePage


if __name__ == "__main__":
    app.run(debug=True)

