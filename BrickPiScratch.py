# BrickPi Interface for Python
#
# Initial Date: June 26, 2013 - Jaikrishna
# Update: June 3, 2014 - Karan Nayan- Exception handling and recovery code added
# Update: March 13, 2016 -	John Cole - EV3 Sensors Integrated.
## 
# This file is for interfacing Scratch with BrickPi
# The Python program acts as the Bridge between Scratch & BrickPi and must be running for the Scratch program to run.
# Requirements :
# Prior to running this progam, ScratchPy must be installed on the system. Refer BrickPi documentation on how to install ScratchPy.
# The BrickPi python library file (BrickPi.py) must be placed in the same path as this file.
# Remote Sensor values must be enabled in Scratch
# This python code must be restarted everytime you need to run a new program. 
# 
# Broadcasts from Python:
# 'READY' tells that BrickPi serial setup succeeded. Use 'When I receive READY' to specify starting point of program. 
# 'UPDATED' tells that sensor values of Scratch has been updated from BrickPi

# Broadcast from Scratch:
# 'SETUP' command sets up the sensor properties
# 'START' command tells RPi to start continuous transmission to BPi
# 'UPDATE' command calls for an updation of Sensor Values of Scratch
# 'STOP' command stops the continuous up
# SETUP and START must be done only once after configuring the Sensors. UPDATE is Required atleast once. 

# Setting Sensor type:

# ULTRASONIC 
# TOUCH
# COLOR
# EV3 ULTRASONIC
# EV3 TOUCH
# EV3 COLOR
# EV3 GYRO
# EV3 INFRARED
# RAW
# FLEX
# TEMP
# Note: Only these sensors are supported as of now. They are lego products except for the last 2 which are from DexterIndustries

# Enabling and Running Motors:
# Enabling motors is no longer necessary
# MA E - Enable motor A
# MB D - Disable motor B
# MA 100 - Set MotorA speed to 100
# MB -50 - Set MotorB speed to -100


import scratch,sys
import math
# import threading

from BrickPi import *
import ir_receiver_check

if ir_receiver_check.check_ir():
	print "Disable IR receiver before continuing!"
	print "Disable IR receiver before continuing!"
	print "Disable IR receiver before continuing!"
	print "Disable IR receiver before continuing!"	
	exit() 

try:
    s = scratch.Scratch()
    if s.connected:
        print "BrickPi Scratch: Connected to Scratch successfully"
	#else:
    #sys.exit(0)
except scratch.ScratchError:
    print "BrickPi Scratch: Scratch is either not opened or remote sensor connections aren't enabled"
    #sys.exit(0)
    
# The sensor types below need to be different for EV3 sensors
# See the Python sensor examples for reference


sensor = [ None, False , False , False , False ]
spec = [ None, 0 , 0 , 0 , 0 ]
running = False
sensorbroadcasts=["S1","S2","S3","S4"]

stype = { 
'EV3US' : TYPE_SENSOR_EV3_US_M0,		# Continuous measurement, distance, cm
'EV3GYRO' : TYPE_SENSOR_EV3_GYRO_M0,			# Angle
'EV3IR' : TYPE_SENSOR_EV3_INFRARED_M0,			# Proximity, 0 to 100
'EV3TOUCH' : TYPE_SENSOR_EV3_TOUCH_DEBOUNCE,	# EV3 Touch sensor, debounced.
'EV3COLOR' : TYPE_SENSOR_EV3_COLOR_M2,
'ULTRASONIC' : TYPE_SENSOR_ULTRASONIC_CONT ,
'TOUCH' : TYPE_SENSOR_TOUCH ,
'COLOR' : TYPE_SENSOR_COLOR_FULL ,
'RAW' : TYPE_SENSOR_RAW,
'TEMP' : TYPE_SENSOR_RAW,
'FLEX' : TYPE_SENSOR_RAW
}   

if BrickPiSetup()==0:
    print "serial connection ok"
else:
    print "serial connection did not start"
    sys.exit()

# activate all motors by default
BrickPi.MotorEnable = [1,1,1,1]
BrickPi.MotorSpeed  = [0,0,0,0]


def comp(val , case):
    if val == None or val== 0:
        return 0
    if case == 1:
        return val-600
    elif case == 2 :
        _a = [0.003357042,         0.003354017,        0.0033530481,       0.0033536166]
        _b = [0.00025214848,       0.00025617244,      0.00025420230,      0.000253772]
        _c = [0.0000033743283,     0.0000021400943,    0.0000011431163,    0.00000085433271]
        _d = [-0.000000064957311, -0.000000072405219, -0.000000069383563, -0.000000087912262]
        RtRt25 = (float)(val) / (1023 - val)
        lnRtRt25 = math.log(RtRt25)
        if (RtRt25 > 3.277) :
                i = 0
        elif (RtRt25 > 0.3599) :
                i = 1
        elif (RtRt25 > 0.06816) :
                i = 2
        else :
                i = 3
        temp =  1.0 / (_a[i] + (_b[i] * lnRtRt25) + (_c[i] * lnRtRt25 * lnRtRt25) + (_d[i] * lnRtRt25 * lnRtRt25 * lnRtRt25))
        temp-=273
        return round(temp,2)



# class myThread (threading.Thread):      #This thread is used for continuous transmission to BPi while main thread takes care of Rx/Tx Broadcasts of Scratch
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
        # print "starting thread"
        # while running:
        #     BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
        #     # for i in range(4):
        #     #     if sensor[i]:
        #     #         if spec[i]:
        #     #             s.sensorupdate({sensorbroadcasts[i] : comp(BrickPi.Sensor[PORT_1+i],spec[i])})
        #     #         else:                
        #     #             s.sensorupdate({sensorbroadcasts[i] : BrickPi.Sensor[PORT_1+i]})
        #     #print BrickPi.Sensor
        #     time.sleep(.2)              # sleep for 200 ms

# thread1 = myThread(1, "Thread-1", 1)        #Setup and start the thread
# thread1.setDaemon(True)


try:
    s.broadcast('READY')
except NameError:
	print "BrickPi Scratch: Unable to Broadcast"
while True:
    try:
        m = s.receive()
        
        while m==None or m[0] == 'sensor-update' :
            m = s.receive()

        msg = m[1].upper()
        if msg == 'SETUP' :
            BrickPiSetupSensors()
            # running = True
            # if thread1.is_alive() == False:
            #     thread1.start()  # this removes the need for the START broadcast
            print "BrickPi Scratch: Setting up sensors done"
            print BrickPi.SensorType
        elif msg == 'START' :
            # running = True
            # if thread1.is_alive() == False:
            #     thread1.start()
            print "BrickPi Scratch: Service Started"
        elif msg == 'STOP' :
            running = False
        elif msg == 'UPDATE' :
            BrickPiUpdateValues()
            for i in range(4):
                if sensor[i]:
                    if spec[i]:
                        s.sensorupdate({sensorbroadcasts[i] : comp(BrickPi.Sensor[PORT_1+i],spec[i])})
                    else:                
                        s.sensorupdate({sensorbroadcasts[i] : BrickPi.Sensor[PORT_1+i]})
            s.broadcast('UPDATED')

        elif msg[:2] in sensorbroadcasts:
            whichsensor = sensorbroadcasts.index(msg[:2])
            if msg[2:].strip() == 'FLEX' :
                spec[whichsensor] = 1
            elif msg[2:].strip() == 'TEMP' :
                spec[whichsensor] = 2
            BrickPi.SensorType[whichsensor+PORT_1] = stype[msg[2:].strip()]
            sensor[whichsensor]=True

        # elif msg[:2] == 'S1' :
        #     if msg[2:].strip() == 'FLEX' :
        #         spec[1] = 1
        #     elif msg[2:].strip() == 'TEMP' :
        #         spec[1] = 2
        #     BrickPi.SensorType[PORT_1] = stype[msg[2:].strip()]
        #     sensor[1] = True
        # elif msg[:2] == 'S2' :
        #     if msg[2:].strip() == 'FLEX' :
        #         spec[2] = 1
        #     elif msg[2:].strip() == 'TEMP' :
        #         spec[2] = 2
        #     BrickPi.SensorType[PORT_2] = stype[msg[2:].strip()]
        #     sensor[2] = True
        # elif msg[:2] == 'S3' :
        #     if msg[2:].strip() == 'FLEX' :
        #         spec[3] = 1
        #     elif msg[2:].strip() == 'TEMP' :
        #         spec[3] = 2
        #     BrickPi.SensorType[PORT_3] = stype[msg[2:].strip()]
        #     sensor[3] = True
        # elif msg[:2] == 'S4' :
        #     if msg[2:].strip() == 'FLEX' :
        #         spec[4] = 1
        #     elif msg[2:].strip() == 'TEMP' :
        #         spec[4] = 2
        #     BrickPi.SensorType[PORT_4] = stype[msg[2:].strip()]
        #     sensor[4] = True
        elif msg == 'MA E' or msg == 'MAE' :
            BrickPi.MotorEnable[PORT_A] = 1
        elif msg == 'MB E' or msg == 'MBE' :
            BrickPi.MotorEnable[PORT_B] = 1
        elif msg == 'MC E' or msg == 'MCE' :
            BrickPi.MotorEnable[PORT_C] = 1
        elif msg == 'MD E' or msg == 'MDE' :
            BrickPi.MotorEnable[PORT_D] = 1
        elif msg == 'MA D' or msg == 'MAD' :
            BrickPi.MotorEnable[PORT_A] = 0
        elif msg == 'MB D' or msg == 'MBD' :
            BrickPi.MotorEnable[PORT_B] = 0
        elif msg == 'MC D' or msg == 'MCD' :
            BrickPi.MotorEnable[PORT_C] = 0
        elif msg == 'MD D' or msg == 'MDD' :
            BrickPi.MotorEnable[PORT_D] = 0
        elif msg[:2] == 'MA' :
            BrickPi.MotorSpeed[PORT_A] = int(msg[2:])
        elif msg[:2] == 'MB' :
            BrickPi.MotorSpeed[PORT_B] = int(msg[2:])
        elif msg[:2] == 'MC' :
            BrickPi.MotorSpeed[PORT_C] = int(msg[2:])
        elif msg[:2] == 'MD' :
            BrickPi.MotorSpeed[PORT_D] = int(msg[2:])
    except KeyboardInterrupt:
        running= False
        print "BrickPi Scratch: Disconnected from Scratch"
        break
    except (scratch.scratch.ScratchConnectionError,NameError) as e:
		while True:
			#thread1.join(0)
			print "BrickPi Scratch: Scratch connection error, Retrying"
			time.sleep(5)
			try:
				s = scratch.Scratch()
				s.broadcast('READY')
				print "BrickPi Scratch: Connected to Scratch successfully"
				break;
			except scratch.ScratchError:
				print "BrickPi Scratch: Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n"
