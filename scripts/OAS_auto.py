from decimal import Clamped
from enum import Enum
from math import atan2, sqrt
from os import wait
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
isDet = detAng = detDist = 0

top : data
## END ##
### END ###

### FUNCTION DEFINITIONS ###

def getAutoValues():
    
    autoData = top.getAutonomousData()
    
    currX, currY , currAZ = autoData[0:2]

    if (shouldAvoid == True):
        targX, targY, targAZ = autoData[3:5]

    # local vars for 
    isDet, detAng, detDist = top.getDetectionData()

def getAngleToTarget():
    return currAZ - atan2(currX - targX, currY - targY)

def getDistanceToTarget():
    return sqrt((currX - targX)^2 + (currY - targY)^2)


currAccel = 0
currVel = 0
def generateMotorCommand(forwPow, turnPow):
    #top.setControlData(Clamped(angleDiffer * 0.5 / MAX_TURN_ANGLE,-1,1), turnDirection)
    pass

def turnTowards():

    angleDiffer = (currAZ - getAngleToTarget())

    # If theres a large difference in between the target and current angle, then 
    if (abs(angleDiffer) > MAX_ANGLE_DIFF):
        angleDiffer = (currAZ - getAngleToTarget())
        turnDirection = 1 if angleDiffer > 0 else -1
        top.setControlData(Clamped(angleDiffer * 0.5 / MAX_TURN_ANGLE,-1,1), turnDirection)
        return 1
    else:
        return 0

def deadOn():

    dist = getDistanceToTarget()

    if (dist > MAX_DIST_DIFF):
        dist = getDistanceToTarget()

        top.setConotrlData(0, Clamped(dist * 0.1 / MAX_TURN_ANGLE,0,1))  
        
        # check if an obstacle was detected
        detection = top.getDetectionData()
        # don't pay attantion to detections that aren't in front of you
        detection = detection[3:4]
        for range in detection:
            if (range != 0):
                return 2

        return 1

    else:
        return 0

def avoid():
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
    wait(500)
    return

### END ###

### MAIN ###

#main loop of code
def main(_top : data):

    top = _top

    getAutoValues()

    while(running):
        if( state == 'idle'):
            print("idling")
            if (getDistanceToTarget):
                state = 'turn'
            wait(0.5)
        elif( state == 'turn'):
            if(turnTowards() == 0):
                top.setControlData(0,0)
                wait(1)
                state = 'deadOn'
        elif( state == 'deadOn'):
            rv = deadOn()
            if (rv == 0):
                if (shouldAvoid):
                    shouldAvoid = False
                    state = 'turn'
                else:
                    state = 'idle'
            elif (rv == 2):
                state = 'avoid'
        elif( state == 'avoid'):
            avoid()
            state = 'turn'


if __name__ == '__main__':
    top = data.OAS_data()
    main(top)

### END ###
