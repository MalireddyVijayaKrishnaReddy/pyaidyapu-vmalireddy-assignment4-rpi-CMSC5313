import time
import threading
import Freenove_DHT as DHT
from gpiozero import Buzzer
import firebase_admin
from firebase_admin import credentials, firestore 
import constants
import firebase_setup
##changes made by other person


db = firestore.client()
collection = firebase_setup.db.collection(constants.COLLECTION_NAME)  
hygrothermographextracredits_ref = collection.document(constants.DOCUMENT_HYGROTHERMOGRAPHEXTRACREDITS)


buzzer = Buzzer(26)


DHTPin = 17  
oldtemperature = 0
buzzer_on = False 


def buzzer_control():
    """ Thread to control buzzer pulsing with 1-second cycle when active """
    global buzzer_on
    while True:
        if buzzer_on:
            buzzer.on()
            time.sleep(0.2)  
            buzzer.off()
            time.sleep(0.2)  
        else:
            buzzer.off()
            time.sleep(0.2)  


def loop():
    global oldtemperature, buzzer_on
    dht = DHT.DHT(DHTPin)  

    while True:
        print("Reading sensor data...")

       
        doc = hygrothermographextracredits_ref.get()
        thresholdTemperature = doc.to_dict().get('ambient_temperature_threshold', 0)

        
        for i in range(15):  
            chk = dht.readDHT11()
            time.sleep(0.1)
            temperature = dht.getTemperature()
            if temperature >= 0:  
                break  

        print(f"Temperature: {temperature:.2f} °C, Threshold: {thresholdTemperature:.2f} °C")

        
        if temperature >= thresholdTemperature:
            buzzer_on = True
            print("Buzzer ON (Pulsing) - Temperature exceeded threshold!")
        else:
            buzzer_on = False
            print("Buzzer OFF - Temperature is normal.")

       
        if oldtemperature != temperature:
            oldtemperature = temperature
            hygrothermographextracredits_ref.update({'ambient_temperature': oldtemperature})

        time.sleep(2)  


if __name__ == '__main__':
    print('Program is starting...')

    
    buzzer_thread = threading.Thread(target=buzzer_control, daemon=True)
    buzzer_thread.start()

    try:
        loop()
    except KeyboardInterrupt:
        buzzer_on = False
        buzzer.off()  
        print("Ending program.")
