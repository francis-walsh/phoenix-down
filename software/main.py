# Declare Imports
import serial
import time
import threading
import matplotlib.pyplot as plt
from playsound import playsound
import os
from datetime import datetime



# Declare Vars
# Plot init
plt.ion()
fig = plt.figure()
sample = []
timeElapsed = []
temperatureData = []
# Sample number
n = 0
maxYRange = 10
maxLength = 50
cropData = True
fancyYLim = True

# Thermistor values
dataBits = 12
VREF = float(3.3)
deltaV = float( VREF/pow(2, dataBits) )
thermistorSlope = float(-59.15236876) # Degrees per volt
thermistorOffset = float(146.1606401) # Degrees

# Values for alarm threshold
regulatedTemperature = 55
alarmThresholdMax = 70
alarmThresholdMin = 20

# Misc
saveLogDirectory = 'logs/'
os.system('cls')
serialToken = "0F"
print("Starting serial...")

# Serial init
ser = serial.Serial('com8', 9600)



# Declare functions
# Woodstove logo
def logo():
	print("---------------------Woodstove--------------------")
	print("**************************************************")
	print("                          ****                    ") 
	print("                       *        *                 ") 
	print("                       * ,****, *                 ") 
	print("                       *        *                 ") 
	print("                       *        *                 ") 
	print("                       *        *                 ") 
	print("                       *        *                 ") 
	print("                       *        *                 ") 
	print("                       *        *                 ") 
	print("                       *        *                 ") 
	print("                  *,   *        *                 ") 
	print("              *   ** *,*        *                 ") 
	print("          *   *,,* **  *        *                 ") 
	print("          * ** *. * ,* **,    *** , *,            ") 
	print("        **,   . ** */(/(**(**(, .*.**   .         ") 
	print("            ***    (**(*,(/ ** **    ****         ") 
	print("          .     ***     ** *,   ,********         ") 
	print("          *****      **     **** ********         ") 
	print("          *********      ***,************         ") 
	print("      *** ********    *.  .**************         ") 
	print("     **   ********     *  .**************         ") 
	print("     **.  ********     *  .**************         ") 
	print("     ***      ******,  *  .**************         ") 
	print("        .*  *     ,*****  .**************         ") 
	print("       ,   ***  *      ,  .*************          ") 
	print("        *,     ***  *     .**********   *         ") 
	print("            .*      ***  *.******     **          ") 
	print("                 *      *****    ,**              ") 
	print("                     *.      ***                  ") 
	print("                         ,*                       ") 
	print("**************************************************")
	print("By Walsh^2 Inc")
	print("Date ", datetime.now())
	print("Temperature is currently being regulated at " + str(regulatedTemperature))
	print("Alarm threshold is between " + str(alarmThresholdMin) + " and " + str(alarmThresholdMax) + " Degrees C")



def saveLog(name):
	print("Saving "+name+" in directory "+saveLogDirectory+"...")
	try:
		file = open(saveLogDirectory+name+".csv", 'x')
	except:
		file = open(saveLogDirectory+name+".csv", 'w')
	file.write("Date,"+str(datetime.now())+"\n")
	file.write("Sample (n),Elapsed Time (s),Temperature (Degrees C)\n")
	for i in range (0, len(sample)):
		file.write(str(sample[i])+","+str(timeElapsed[i])+","+str(temperatureData[i])+"\n")
	file.close()
	print("File saved!")



# Audible alarm function
def playAlarm(numberOfTimes):
	for i in range(0, numberOfTimes):
		playsound('peep.mp3')
		
	
# Send byte over serial
# Byte should be of the form 0x[XX]
def writeByte(byte):
	ser.write(bytes.fromhex(serialToken+' '+str(byte)))



# Serial write thread
def commandThread():
	print("Enter 'help' or 'h' for a list of commands")
	while(True):
		temp = input("=>")
		
		
		
		# Example commands
		# Easter egg
		if(temp == "bird"):
			playAlarm(3)
			
		if(temp == "help" or temp == "h"):
			print("t					- Displays current temperature")
			print("setTemp [num]		- Sets target temperature to [num]")
			print("setMaxThreshold [num]- Sets maximum threshold for alarm to [num]")
			print("setMinThreshold [num]- Sets minimum threshold for alarm to [num]")
			print("sampleCrop			- Toggles x axis cropping")
			print("sampleLength [num]	- Sets the length of x axis to [num]")
			print("fancyLims			- Toggles y axis cropping")
			print("ping					- Arduino should respond with 'pong' if connected correctly")
			print("saveas [name]		- Saves the logged data in a csv file [name].csv")
			print("clr					- Clears terminal")
		
		
		if(temp == "t"):
			print(temperatureData[len(temperatureData)-1])
			
		if("setTemp" in temp):
			byteData = str(hex(int(temp.replace("setTemp ", ""))))[2:]
			if(len(byteData) <= 1):
				byteData = '0'+byteData
			writeByte(byteData)
			
		if(temp == "sampleCrop"):
			global cropData
			cropData = not cropData
		
		if("sampleLength" in temp):
			global maxLength
			maxLength = int(temp.replace("sampleLength ", ""))
		
		if(temp == "fancyLims"):
			global fancyYLim
			fancyYLim = not fancyYLim
		
		if("saveas" in temp):
			saveLog(temp.replace("saveas ", ""))
			
		if("setMinThreshold" in temp):
			global alarmThresholdMin
			alarmThresholdMin = int(temp.replace("setMinThreshold ", ""))
		
		if("setMaxThreshold" in temp):
			global alarmThresholdMax
			alarmThresholdMax = int(temp.replace("setMaxThreshold ", ""))
		
		if(temp == 'clr'):
			os.system('cls')
			logo()
			
		if(temp == "ping"):
			writeByte('FF')
		

# Start program here...
# Print logo
logo()
startTime = time.time()

# Start threads
p1 = threading.Thread(target=commandThread)
p1.start()



# Serial read loop
while(True):
	# Gather data
	data = ser.readline()
	data = data.decode()
	data = data.split(',')
	
	# Ping Pong statement
	if("pong" in str(data)):
		print("pong\n")
		playAlarm(1)
	
	
	
	# Convert data into temperature
	temperature = -999
	if(len(data) == 2):
		temperature = data[1].replace("Data:", "").replace("\r\n", "").replace(" ", "")
		# print("Hex: " + str(temperature))
		temperature = int(temperature, 16)
		# print("Des: " + str(temperature))
		temperature = float( thermistorSlope*(temperature*deltaV)+thermistorOffset )
		# print("Temp: " + str(temperature))
		
		
		
		# *** PUT ALARM CASES HERE ***
		if(temperature < alarmThresholdMin or temperature > alarmThresholdMax):
			print("WARNING!!!")
			print("TEMPERATURE AT " + str(temperature))
			print("SENDING OFF COMMAND")
			playAlarm(int(5))
			ser.write()
	
	
		
	# Plot temperature
	if(temperature < 100 and temperature > -5):
		# Plot functions
		sample.append(n)
		timeElapsed.append(time.time()-startTime)
		temperatureData.append(temperature)
		n+=1
		
		# Format data to look pretty
		x = sample
		y = temperatureData
		
		# Crop data
		if(int(len(x)) > int(maxLength) and cropData):
			x = x[len(x)-maxLength:len(x)]
			y = y[len(y)-maxLength:len(y)]
		
		plt.cla()
		plt.plot(x, y, color='red', label='Temperature')
		if(fancyYLim == True):
			plt.ylim([y[len(y)-1]-maxYRange, y[len(y)-1]+maxYRange])
		else:
			plt.ylim([0, 50])
		plt.title("WoodStove Temperature")
		plt.xlabel("Sample Number")
		plt.ylabel("Temperature (Degrees C)")
		plt.grid()
		plt.show()
		plt.pause(0.0001)
	
