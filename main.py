from lcdFunctions import LCDClass
from dictionaries import units, xyModes
from bluetoothConnection import BluetoothComm
import threading
import struct
import math
import time
import subprocess



f = open( "/dev/input/mice", "rb" ); 
# Open the file in the read-binary mode

quadrentCodes = [8,24,56,40]
leftClickCodes = []
rightClickCodes = []
midClickCodes = []
midLeftCodes = []
midRightCodes = []

unit = list(units.keys())[0]
mode = xyModes[0]

for elem in quadrentCodes:
  leftClickCodes.append(elem+1)
  rightClickCodes.append(elem+2)
  midClickCodes.append(elem+4)
  midLeftCodes.append(elem+5)
  midRightCodes.append(elem+6)

distanceDots = 0
lcd = LCDClass()

currentUnitIndex = 0
currentModeIndex = 0
bluetoothConnected = False
blue_com = None

unitKeys = list(units.keys())
unit = unitKeys[currentUnitIndex]
mode = xyModes[currentModeIndex]


class lcdUpdatingThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      global distanceDots

      prevDots = 0
      while (1):
        lcd.updateDistanceOnLcd(distanceDots, units[unit])

        if (prevDots == distanceDots):
          time.sleep(0.1)
        else:
          time.sleep(0.01)

        prevDots = distanceDots


def current_milli_time():
    return round(time.time() * 1000)

def cycleUnits():
  global unit, currentUnitIndex
  if currentUnitIndex < len(unitKeys) - 1 :
    currentUnitIndex = currentUnitIndex + 1
    unit = unitKeys[currentUnitIndex]
  else: 
    currentUnitIndex = 0
    unit = unitKeys[currentUnitIndex]

def cycleModes():
  global mode, currentModeIndex
  if currentModeIndex < len(xyModes) - 1:
    currentModeIndex = currentModeIndex + 1
    mode = xyModes[currentModeIndex]
  else:
    currentModeIndex = 0
    mode = xyModes[currentModeIndex]






def incrementDots(increment): 
  global distanceDots 
  distanceDots = distanceDots + increment

def resetDots():
  global distanceDots
  distanceDots = 0


def updateDistanceOnStream(distanceDots, divisor):

  if (bluetoothConnected):
    blue_comm.send_comm(str(distanceDots));
    blue_comm.send_comm('\r\n');

def bluetoothConnection():
  global blue_comm, bluetoothConnected
  while 1:
    data = f.read(3)
    tuple = struct.unpack('3b',data)

    if tuple[0] in rightClickCodes:
      lcd.displayMessage("Connecting")
      blue_comm = BluetoothComm()
      lcd.displayMessage("Connected")
      bluetoothConnected = True
      break
      
    
    elif tuple[0] in midClickCodes:
      lcd.displayMessage("Not Connected")
      break

def pair():
  while 1:
    data = f.read(3)
    tuple = struct.unpack('3b',data)

    if tuple[0] in rightClickCodes:
      lcd.displayMessage("Pairing")
      subprocess.call(['bash', './pairing.sh'])
      lcd.displayMessage("Paired")
      time.sleep(2);
      break
      
    
    elif tuple[0] in midClickCodes:
      lcd.displayMessage("Not Paired")
      break
  

def checkDoubleClick(currentTime, prevTime, currentCode, prevCode):
  
  if ((currentTime - prevTime)/1000 <= 0.3 and currentCode == prevCode):   
    return True
  else:
    return False



def main():
  global bluetoothConnected
  lcd.displayQuestion("Pair to BT?")

  pair()

  lcd.displayQuestion("Connect to BT?")
  
  
  bluetoothConnection()

  time.sleep(2)
  lcd.clear()
  global distanceDots

  lcd.updateModeOnLcd(mode)
  lcd.updateUnitOnLcd(unit)
  lcd.updateDistanceOnLcd(0,1)

  prevClickTime = 0
  currentClickTime = 0
  prevClickCode = 0

  thread1 = lcdUpdatingThread(1, "Thread-1", 1)
  thread1.start()

  while 1:
    data = f.read(3)  # Reads the 3 bytes 
    
    tuple = struct.unpack('3b',data)

    currentClickTime = current_milli_time()
    if tuple[0] in rightClickCodes:

      if (checkDoubleClick(currentClickTime, prevClickTime, tuple[0], prevClickCode) and tuple[1] == 0 and tuple[2] == 0):
        cycleUnits()
        lcd.updateUnitOnLcd(unit)
        updateDistanceOnStream(distanceDots, units[unit])

      prevClickTime = currentClickTime
      prevClickCode = tuple[0]

      if currentModeIndex == 0:
          incrementDots(math.sqrt( tuple[1]**2 + tuple[2]**2))
      elif currentModeIndex == 1:
          incrementDots( tuple[1] )
      elif currentModeIndex == 2:
          incrementDots( abs(tuple[1]) )
      elif currentModeIndex == 3:
          incrementDots( tuple[2] )
      elif currentModeIndex == 4:
          incrementDots( abs(tuple[2]) )
      else:
          incrementDots(math.sqrt( tuple[1]**2 + tuple[2]**2))

      updateDistanceOnStream(distanceDots, units[unit])

    elif tuple[0] in midClickCodes:
      cycleModes()
      lcd.updateModeOnLcd(mode)

    elif tuple[0] in midRightCodes:
      resetDots()
      updateDistanceOnStream(distanceDots, units[unit])


try:
  if __name__ == "__main__": main()
except Exception as e:
  print(e)
  lcd.displayMessage("Something wrong\n restart")
  
