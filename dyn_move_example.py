#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# In Class Assignment 3 - PID Controller
# 11/11/14

# ******************************************************

import controller_include as ci
import time
import math
import ach
from ctypes import *

c = ach.Channel(ci.CONTROLLER_REF_NAME)
c.flush()
d = ach.Channel(ci.DYNAMIXL_CTRL_NAME)
d.flush()
err = ci.CONTROLLER_REF()
dmxl = ci.DYNAMIXL_REF()

lastEx = 0
lastEy = 0
lastT = 0.01
px = 0
ix = 0
dx = 0
py = 0
iy = 0
dy = 0


kp = .00015		# 1.1
ki = .000015		# 0.15
kd = .00007		# 0.5

#kp = .00015
#ki = 0
#kd = 0

while 1:
	[status, framesize] = c.get(err, wait=True, last=True)
	# Praportional Control
	px = float(err.x)
	py = float(err.y)
	
	# Integral Control
	ix += px
	iy += py
	tim = time.time()
	# Derivative Control
	dx = float(err.x - lastEx) / (tim - lastT)
	dy = float(err.y - lastEy) / (tim - lastT)
	lastEx = err.x
	lastEy = err.y
	lastT = tim
	
	# Controller output
	ys = px*kp + ix*ki + dx*kd
	ps = py*kp + iy*ki + dy*kd
	if ys > 1:
		ys = 1
	elif ys < -1:
		ys = -1
	if ps > 1:
		ps = 1
	elif ps < -1:
		ps = -1

	dmxl.yaw_speed = int(ys * 800)
	dmxl.yaw_dir = math.copysign(1.6, -dmxl.yaw_speed)
	dmxl.yaw_speed = abs(dmxl.yaw_speed)
	dmxl.pitch_speed = int(ps * 800)
	dmxl.pitch_dir = math.copysign(1.6, -dmxl.pitch_speed)
	dmxl.pitch_speed = abs(dmxl.pitch_speed)
	#dmxl.pitch_dir = 0
	#dmxl.pitch_speed = 0
	if dmxl.yaw_dir < 0:
		print -dmxl.yaw_speed, px, ix, dx
	else:
		print dmxl.yaw_speed, px, ix, dx
    	d.put(dmxl)
    	
c.close()
d.close()














