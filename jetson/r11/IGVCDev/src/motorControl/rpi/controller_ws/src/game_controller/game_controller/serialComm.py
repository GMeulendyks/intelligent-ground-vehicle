import serial
import time

startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
messageComplete = False

#========================
#========================
    # the functions

def setupSerial(baudRate, serialPortName):
    
    global  ser
    
    ser = serial.Serial(port= serialPortName, baudrate = baudRate, timeout=0, rtscts=True)

    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

    # waitForArduino()

#========================

def sendToArduino(ser, message):

    
    # message = "<motor, " + str(50) + ", " + str(50) + ">"
    ser.write(message.encode('UTF-8'))


#==================

def recvLikeArduino():

    global startMarker, endMarker, ser, dataStarted, dataBuf, messageComplete

    if ser.inWaiting() > 0 and messageComplete == False:
        x = ser.read().decode("utf-8") # decode needed for Python3
        
        if dataStarted == True:
            if x != endMarker:
                dataBuf = dataBuf + x
            else:
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataBuf = ''
            dataStarted = True
    
    if (messageComplete == True):
        messageComplete = False
        return dataBuf
    else:
        return "XXX" 

#==================

def waitForArduino():

    # wait until the Arduino sends 'Arduino is ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded
    
    print("Waiting for Arduino to reset")
     
    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == 'XXX'): 
            print(msg)



#====================
#====================
    # the program


def run():
    setupSerial(115200, "/dev/ttyACM0")
    sendToArduino()
    # setupSerial(115200, "/dev/ttyACM0")
    # count = 0
    # prevTime = time.time()
    # while True:
    #             # check for a reply
    #     arduinoReply = recvLikeArduino()
    #     if not (arduinoReply == 'XXX'):
    #         print ("Time %s  Reply %s" %(time.time(), arduinoReply))
            
    #         # send a message at intervals
    #     if time.time() - prevTime > 1.0:
    #         sendToArduino()
    #         prevTime = time.time()
    #         count += 1
