BrickPi Scratch Code and Examples
===================

This repository contains a Scratch library for BrickPi and Raspberry Pi, allowing you to use Scratch and LEGO Mindstorms NXT motors and sensors.
These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

Installation
============

For step by step instructions on how to use Scratch with the BrickPi, please see our [tutorial on getting started with Scratch.](http://www.dexterindustries.com/BrickPi/program-it/scratch/)

Video and text tutorials for installation and operation are provided.

See Also
========

[BrickPi](http://www.dexterindustries.com/BrickPi.html) is a [Raspberry Pi](http://www.raspberrypi.org) Board that connects [LEGO MINDSTORMS motors and sensors](http://mindstorms.lego.com) to the Raspberry Pi.

More information on hardware, firmware, and software can be found on the [BrickPi site](http://www.dexterindustries.com/BrickPi)

The BrickPi can be [purchased here.](http://www.dexterindustries.com/BrickPi.html)


=======
BrickPi
=======

BrickPi is a package that provides access to the BrickPi Raspberry Pi extension board.  
The BrickPi extension board is a microprocessor board that allows the Raspberry Pi to 
communicate with LEGO Mindstorms motors and sensors.  The package provides Python and 
Scratch interfaces to the BrickPi.


Scratch interface
=================

The Scratch interface is via a BrickPiScratch class that inherits from GenericDevice,
where GenericDevice is a plugin base class in the RpiScratchIO package.


RpiScratchIO configuration file
-------------------------------

The Scratch interface uses scratchpy via RpiScratchIO.  Sensors should be added by 
declaring them in the configuration file::

    [DeviceTypes]
    LEGO = import BrickPi; from BrickPi.BrickPiScratch import BrickPiScratch; BrickPiScratch()

    [DeviceConnections]
    LEGO = UART0

    [BrickPi]
    S1 = ULTRASONIC_CONT
    MA =
    MB =

In this example, one ultrasonic sensor and two motors are attached to the BrickPi.  
Motors can be added to the MC or MD ports by declaring them in the same manner.  Sensors 
can be added by assigning the senors names to the sensor ports (S1 to S4).  The available
sensor names are::

    TOUCH
    ULTRASONIC_CONT
    ULTRASONIC_SS
    RCX_LIGHT
    COLOR_FULL
    COLOR_RED
    COLOR_GREEN
    COLOR_BLUE
    COLOR_NONE
    I2C
    I2C_9V

When instantiated, the BrickPiScratch class starts a separate thread to update values 
between the BrickPi and the Raspberry Pi at a rate of 10Hz.  Values can then be read 
from the Raspberry Pi on demand or within the data acquisition loop.  To configure the 
automatic readout to Scratch during the data acquisition loop, the readout period can be 
stated in the configuration file::

    LEGO = import BrickPi; from BrickPi.BrickPiScratch import BrickPiScratch; BrickPiScratch(5)

where this line should replace the constructor line in the previous example and the number 
5 is the readout period.  This means that the sensor or motor encoder values will be 
updated in Scratch once for every five readout loops.  Since the readout loop runs at 
10Hz, this implies that the sensors in Scratch are updated at a rate of 2Hz.  For a 
simple Scratch program running on the Raspberry Pi, a 2Hz update rate is the maximum 
that Scratch can process without a delay.

Sensors or motor encoders can be added to the automatic readout loop by using 
the channel number (explained later) or "s" (for all sensors) or "m" (for all motor 
encoders) or "all" (for both sensors and motor encoders).  The period and sensors can also 
be added from Scratch by using the config broadcast command (explained later).  To prevent the 
automatic update of sensors or motor encoders when Scratch starts, set the readout 
period to 0::

    LEGO = import BrickPi; from BrickPi.BrickPiScratch import BrickPiScratch; BrickPiScratch(0,"S")

where the active sensor channels have all been added in this case too.

Access from Scratch
-------------------

Start Scratch from the command line or the menu.  Then enable the remote sensor 
connections by right clicking on the *sensor value* text, which can be found under the 
*Sensing* tool palette.  A dialog box should appear to say that the remote sensor 
connections have been enabled.  At this point, Scratch becomes a server.  Do not run 
more than one Scratch window on the same machine, otherwise only the first one will be 
accessible from the Python API.  When Scratch has been started, type::

    RpiScratchIO configFile.cfg

where *configFile.cfg* should be replaced with the name of the configuration file that 
was created in the previous step.  If the name of the configuration file is omitted, 
then RpiScratchIO will try to use RpiScratchIO.cfg instead.

When RpiScratchIO starts, it loads the BrickPiScratch Python class.  This updates 
Scratch with several new sensors.  Using the example configuration files given above, 
the variables are::

    LEGO:0
    LEGO:1
    LEGO:2
    LEGO:3
    LEGO:10
    LEGO:11
    LEGO:12
    LEGO:13
    LEGO:20
    LEGO:21
    LEGO:22
    LEGO:23

where these correspond to the sensor ports S1-S4 (0-3), motor ports MA-MD (10-13) and 
motor encoder ports MA-MD (20-23).  The motor channels (10-13) contain the value that was 
written to the motors.  Values can be read into the sensor values on demand by sending a 
Scratch broadcast message of the form::

    LEGO:read:0

where 0 is the channel number (S1 in this case).  The value will then appear in the 
corresponding sensor approximately 0.2s later.

Values can be written to the motors by sending a Scratch broadcast request of the form::

    LEGO:write:10,200 

where 10 is the channel number (MA in this case) and 200 is the motor speed value.

Scratch can be used to enable the automatic updating of enabled sensor values by broadcasting::

    LEGO:config:update,s

where the list of channels or wild card options (s for all sensors, m for all motor 
encoders or a list of channels separated by spaces), should follow update.  The rate of 
the update can be set from Scratch by broadcasting::

    LEOG:config:period,5

where 5 implies 2Hz and 10 implies 1Hz etc.  To disable the automatic readout, the 
period should be set to 0.