from flask import Flask, render_template
import os
from threading import Thread
from nrf24 import NRF24
BASE_DIR = os.path.join(os.path.dirname(__file__))
app = Flask(__name__, static_url_path=BASE_DIR + 'static')
app.debug = True

generic = []

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
radio = NRF24()
def installNrf():
    global radio
    radio.begin(1,0,"P9_23", "P9_24") #Set CE and IRQ pins
    radio.setRetries(15,15)
    radio.setPayloadSize(8)
    radio.setChannel(100)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MAX)
    radio.setCRCLength(NRF24.RF24_CRC_16)
    radio.openWritingPipe(0xF0F0F0F0E1) 
    radio.openReadingPipe(1,0xF0F0F0F0D2)
        
def nodeChecker():
    global radio
    installNrf()
    radio.startListening()
    
    while True:
        pipe = [0]
        while not radio.avaliable(pipe, True):
            pass
        recv = []
        radio.read(recv)
        
        print recv
t = Thread(target=nodeChecker)
t.start()