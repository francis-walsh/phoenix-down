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

# Misc
saveLogDirectory = 'logs/'
os.system('cls')
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



def saveLog(name):
	print("Saving "+name+" in directory "+saveLogDirectory+"...")
	try:
		file = open(saveLogDirectory+name+".csv", 'x')
	except:
		file = open(saveLogDirectory+name+".csv", 'w')
	file.write("Date,"+str(datetime.now())+"\n")
	file.write("Sample (n),Elapsed Time(s),Temperature (Degrees C)\n")
	for i in range (0, len(sample)):
		file.write(str(sample[i])+","+str(timeElapsed[i])+","+str(temperatureData[i])+"\n")
	file.close()
	print("File saved!")



# Audible alarm function
def playAlarm(numberOfTimes):
	for i in range(0, numberOfTimes):
		playsound('peep.mp3')



# Serial write thread
def commandThread():
	print("Enter 'help' or 'h' for a list of commands")
	while(True):
		temp = input("Command:\n")
		ser.write(str.encode(temp))
		# *** FIRMWARE FUNCTIONS HERE ***
		# Make ping - pong function
		# Make temperature setpoint function
		# Make make alarm threshold function
		# Make PID Loop configurations?
		
		
		
		# Example commands
		# Easter egg
		if(temp == "bird"):
			playAlarm(3)
			
		if(temp == "help" or temp == "h"):
			print("t			- Displays current temperature")
			print("sampleCrop		- Toggles x axis cropping")
			print("sampleLength		- Sets the length of x axis cropping")
			print("fancyLims		- Toggles y axis cropping")
			print("saveas [name]		- Saves the logged data in a csv file [name].csv")
		
		if(temp == "t"):
			print(temperatureData[len(temperatureData)-1])
			
		if(temp == "sampleCrop"):
			global cropData
			cropData = not cropData
		
		if(temp == "sampleLength"):
			global maxLength
			maxLength = int(input("Display Length\n"))
		
		if(temp == "fancyLims"):
			global fancyYLim
			fancyYLim = not fancyYLim
		
		if("saveas" in temp):
			saveLog(temp.replace("saveas ", ""))
		

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
	
	
	# *** PUT ALARM CASES HERE ***
	
	
	# Convert data into temperature
	temperature = -999
	if(len(data) == 2):
		temperature = data[1].replace("Data:", "").replace("\r\n", "").replace(" ", "")
		# print("Hex: " + str(temperature))
		temperature = int(temperature, 16)
		# print("Des: " + str(temperature))
		temperature = float( thermistorSlope*(temperature*deltaV)+thermistorOffset )
		# print("Temp: " + str(temperature))
		
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
	
