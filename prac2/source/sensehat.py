from sense_emu import SenseHat
import time
import datetime
import numpy as np
import json
import os
from pathlib import Path

sense = SenseHat()

green = (0, 128, 0)
red = (128, 0, 0)
blue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)

speed = 0.04

print("AmbSnooper v0.2b")

def update_screen():
    now = datetime.datetime.now()
 
    temp = sense.temp
    temp_disp = str.format("%.2f" % temp)
 
    pressure = sense.pressure
    pressure_disp = str.format("%.2f" % pressure)
 
    humidity = sense.humidity
    humidity_disp = str.format("%.2f" % humidity)

    print("Fecha y hora: " + now.strftime("%Y-%m-%d %H:%M:%S"))
    print("Temp:" + temp_disp + " C")
    print("Pres:" + pressure_disp + " mB")
    print("Hum:" + humidity_disp + " %")

    sense.show_message("Hora y fecha: " + now.strftime("%Y-%m-%d %H:%M:%S"), scroll_speed=speed, back_colour = black)
    sense.show_message(temp_disp + " C", scroll_speed=speed, back_colour = red)
    sense.show_message(temp_disp + " mB", scroll_speed=speed, back_colour = green)
    sense.show_message(temp_disp + " %", scroll_speed=speed, back_colour = blue)

    sense.set_pixels(np.zeros((64, 3), dtype=np.uint8))

def getRocioPoint(T,H):
    A = 17.271
    B = 237.7
    
    gamma = (A * T / (B + T)) + np.log(H/100.0)
    rocio = (B * gamma) / (A - gamma)
    
    return rocio

def writeJson():
    parentPath = str(Path(os.getcwd()).parent.absolute())
    targetPath = parentPath + "/data"
    
    if os.path.isdir(targetPath) == False:
        os.mkdir(parentPath + "/data")
    
    now = datetime.datetime.now()
    
    outputJson = {
        "NombreGrupo":"Francisco Jesus Sanchez Rubio",
        "Timestamp":str(now.strftime("%Y-%m-%d %H:%M:%S")),
        "Temp":str(sense.temp),
        "Hum":str(sense.humidity),
        "Press":str(sense.pressure),
        "Tdpr":str(getRocioPoint(sense.temp,sense.humidity))
        }
    
    jsonObj = json.dumps(outputJson, indent=4)
    with open(targetPath + "/senseHat" + now.strftime("%Y%m%d-%H%M%S") + ".json","w") as outfile:
        outfile.write(jsonObj)
    

while True:
    events = sense.stick.get_events()
    for event in events:
        if event.action == "released" and event.direction == "down":
            writeJson()
            update_screen()
            
    time.sleep(0.1)
    
 


