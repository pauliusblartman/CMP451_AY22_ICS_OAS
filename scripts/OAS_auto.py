from decimal import Clamped
from enum import Enum
from math import atan2, sqrt
import numpy as np
from os import wait
import time
import OAS_data as data



### ENUM DECLARATION ###

class CoStatelor(Enum):

    idle = 1

    deadOn = 2

    avoid = 3

state = 'idle'

### END ###


### CONSTANTS DECLATIONS ###
# coverage of sensor array
COVERAGE = 30
MAX_ANGLE_DIFF = 5
MAX_DIST_DIFF = 1
MAX_TURN_ANGLE = 15
MAX_SPEED = 0.25



### FIELD DECLARATIONS ###

## PRIVATE ##

# control whether the main loop is currently executing
running = True

shouldAvoid = False

# local accessors for getting individual data
currX = currY = currAZ = 0
targX = targY = targAZ = 0

# local vars for 
#isDet = detAng = detDist = 0

top : data.OAS_data
## END ##
### END ###

### FUNCTION DEFINITIONS ###

def getAutoValues():
    
    global currX, currY, currAZ, targX, targY, targAZ, shouldAvoid, top
    
    autoData = top.getAutonomousData()
    #print ("[AUTO]: Gotten Auto Data ", autoData)
    currX, currY  = autoData[0:2]

    if (shouldAvoid == True):
        targX, targY, targAZ = autoData[2:5]
        
    currAZ = autoData[5] - 180
    
    #print ("cuuAZ: ", currAZ, " expected AZ", autoData[5] )

    # local vars for 
    #isDet, detAng, detDist = top.getDetectionData()

def getAngleToTarget():
    global currX, currY, currAZ, targX, targY, targAZ, shouldAvoid, top
    diff = np.rad2deg(atan2(currX - targX, currY - targY))
    
    return diff

def getDistanceToTarget():
    global currX, currY, currAZ, targX, targY, targAZ, shouldAvoid, top
    return sqrt(pow(currX - targX,2) + pow(currY - targY,2))


currAccel = 0
currVel = 0

def generateMotorCommand(forwPow, turnPow):
    #top.setControlData(Clamped(angleDiffer * 0.5 / MAX_TURN_ANGLE,-1,1), turnDirection)
    top.setControlData([np.clip(angleDiffer * 0.0 / 180,-0.5,0.5), turnDirection])
    pass

def turnTowards():

    global currX, currY, currAZ, targX, targY, targAZ, shouldAvoid, top

    angleDiffer = (currAZ - getAngleToTarget())

    print ("[AUTO]: Current Angle ", currAZ)
    
    print ("[AUTO]: Target Angle ", getAngleToTarget())
    
    print ("[AUTO]: Current Angle Diff", angleDiffer)

    # If theres a large difference in between the target and current angle, then 
    if (abs(angleDiffer) > MAX_ANGLE_DIFF):
        angleDiffer = (currAZ - getAngleToTarget())
        turnDirection = 1 if angleDiffer > 0 else -1
        #top.setControlData([np.clip(angleDiffer * 0.0 / 180,-0.5,0.5), turnDirection])
        top.setControlData([0.5, turnDirection])
        return 1
    else:
        return 0


startDist = 0

def deadOn():

    global currX, currY, currAZ, targX, targY, targAZ, shouldAvoid, top, startDist

    dist = getDistanceToTarget()

    if (startDist == 0):
        startDist = dist

    if (dist > MAX_DIST_DIFF):
        dist = getDistanceToTarget()

        top.setControlData([0.6,0])  
        
        # check if an obstacle was detected
        detection = top.getDetectionData()
        
        if (dist - startDist > 2):
            startDist = 0
            return 3
        
        # don't pay attantion to detections that aren't in front of you
        detection = detection[3:4]
        for range in detection:
            if (range != 0):
                return 2

        return 1

    else:
        return 0

def avoid():
    
    global currX, currY, currAZ, targX, targY, targAZ, shouldAvoid, top
    
    #currX, currY , currAZ, targX, targY, targAZ
    # check if an obstacle was detected
    detection = top.getDetectionData()
    
    opening = -1
    # find the closest opening
    for i in range(3):
        if (detection[2 - i] == 0):
            opening = 2 - 1
        elif (detection[3 + i] == 0):
            opening = 3 + i

    if (opening == -1):
        #vectorToObstacle = 
        #targX = Axcosθ+Aysinθ
        #targY = −Axsinθ+Aycosθ
        pass
    time.sleep(500)
    return

### END ###

### MAIN ###

#main loop of code
def main(_top : data.OAS_data):
    
    global currX, currY, currAZ, targX, targY, targAZ, shouldAvoid, top
    
    top = _top
    

    state = 'idle'
    
    shouldAvoid = False


    while(running):
        getAutoValues()
        if( state == 'idle'):
            print("idling")
            #if (getDistanceToTarget() > MAX_DIST_DIFF):
            state = 'turn'
            time.sleep(0.5)
        elif( state == 'turn'):
            print("turning")
            if(turnTowards() == 0):
                top.setControlData([0,0])
                time.sleep(1)
                state = 'deadOn'
        elif( state == 'deadOn'):
            print("striaghting")
            rv = deadOn()
            if (rv == 0):
                if (shouldAvoid):
                    shouldAvoid = False
                    state = 'turn'
                else:
                    state = 'idle'
            elif (rv == 2):
                state = 'avoid'
            elif (rv == 3):
                state = 'turn'
                time.sleep(0.5)
        elif( state == 'avoid'):
            print("avoid it")
            avoid()
            state = 'turn'
        else:
            state = 'idle'
        time.sleep(0.1)
if __name__ == '__main__':
    top = data.OAS_data()
    main(top)

### END ###
