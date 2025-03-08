import time
import Freenove_DHT as DHT
import firebase_admin
from firebase_admin import credentials, firestore 
import constants
import firebase_setup

db = firestore.client()
collection = firebase_setup.db.collection(constants.COLLECTION_NAME)  
hygrothermograph_ref = collection.document(constants.DOCUMENT_HYGROTHERMOGRAPH)

DHTPin = 17  
oldtemperature=0
oldhumidity=0

def loop():
    global oldhumidity
    global oldtemperature
    dht = DHT.DHT(DHTPin) 
     

    while True:
        #counts += 1
        #print("Measurement counts: ", counts)
        
        for i in range(0, 50):
            chk = dht.readDHT11()  
            
            time.sleep(0.1)
            humidity =    dht.getHumidity()
            temperature=  dht.getTemperature()
            if humidity<0:
                continue
            
        
        print("Humidity : %.2f, \t Temperature : %.2f \n" % (humidity, temperature))
        if oldhumidity!=humidity or oldtemperature!=temperature:
            oldhumidity=humidity
            oldtemperature=temperature
            if humidity>=0: 
                hygrothermograph_ref.update({'humidity': oldhumidity,'temperature':oldtemperature})
           
        time.sleep(2)

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        exit()
