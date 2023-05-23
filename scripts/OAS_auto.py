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

# local accessors for getting individual data
currX = currY = currAZ = 0
targX = targY = targAZ = 0

# local vars for 
isDet = detAng = detDist = 0

top : data
## END ##
### END ###

### FUNCTION DEFINITIONS ###

def getAngleToTarget():
    return currAZ - atan2(currX - targX, currY - targY)

def getDistanceToTarget():
    return sqrt((currX - targX)^2 + (currY - targY)^2)


def turnTowards():

    angleDiffer = (currAZ - getAngleToTarget())

    # If theres a large difference in between the target and current angle, then 
    while (abs(angleDiffer) > MAX_ANGLE_DIFF):
        angleDiffer = (currAZ - getAngleToTarget())
        top.setControlData(0, Clamped(angleDiffer * 0.5 / MAX_TURN_ANGLE,-1,1))
    return

def deadOn():

    dist = getDistanceToTarget()

    while (dist > MAX_DIST_DIFF):
        dist = getDistanceToTarget()



        top.setConotrlData(0, Clamped(dist * 0.5 / MAX_TURN_ANGLE,0,1))  
        
        # check if an obstacle was detected
        isDet, detAng, detDist = top.getDetectionData()
        if (isDet):
            return 1

    else:
        return 0

def avoid():
    top.setControlData(0, 0)  
    wait(500)
    return

### END ###

### MAIN ###

#main loop of code
def main(_top : data):

    top = _top

    while(running):
        if( state == 'idle'):
            print("idling")
            wait(0.5)
        elif( state == 'turn'):
            turnTowards()
            state = 'deadOn'
        elif( state == 'deadOn'):
            if (deadOn() == 1):
                state = 'avoid'
            else:
                state = 'idle'
        elif( state == 'avoid'):
            avoid()
            state = 'deadOn'


if __name__ == '__main__':
    top = data.OAS_data()
    main(top)

### END ###
