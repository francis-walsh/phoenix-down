# phoenix-down

![alt text](https://github.com/DanielDW5555/phoniex-down/blob/main/photos/PCBA.PNG)

Phoenix Down is a PWM-controlled hot plate that regulates the temperature of your morning coffee. A 12V 2A voltage source is regulated by a buck converter to deliver a maximum of 24W to the array of power resistors, heating the board to a specified temperature monitored by a thermistor. The design uses a schmitt trigger, astable multivibrator, and a thermistor to configure the duty cycle of the PWM.

The computer has population options for different thermistors and voltage references for configuring the thermistor voltage threshold.

Rev 1 schematic
![alt text](https://github.com/DanielDW5555/phoniex-down/blob/main/photos/sch.PNG)

Rev 1 TLspice simulation
![alt text](https://github.com/DanielDW5555/phoniex-down/blob/main/photos/LTspice.PNG)
