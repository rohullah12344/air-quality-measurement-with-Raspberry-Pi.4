from mq import *
from urllib.request import urlopen
import RPi.GPIO as GPIO
import dht11
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=14)
API = "X6UBWOZQPCJ31REM" 
URL = "https://api.thingspeak.com/update?api_key={}".format(API)
try:
    print("Press CTRL+C to abort.")
    mq = MQ();
    while True:
        result = instance.read()
        if result.is_valid():
            perc = mq.MQPercentage()
            print("Sıcaklık:{}C  Nem:{}%  LPG:{}pmm  CO:{}pmm  Duman:{}pmm ".format(result.temperature,result.humidity,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
            thingspeakHttp =URL + "&field1={}&field2={}&field3={}&field4={}&field5={}".format(result.temperature,result.humidity,perc["GAS_LPG"], perc["CO"], perc["SMOKE"])
            conn = urlopen(thingspeakHttp)  
            time.sleep(1)
except:
    print("\nSonlandirildi")
    GPIO.cleanup()