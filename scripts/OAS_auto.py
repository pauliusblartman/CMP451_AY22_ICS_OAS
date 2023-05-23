from enum import Enum
from os import wait
from simple_pid import PID
import Lock



### ENUM DECLARATION ###

class CoStatelor(Enum):

    idle = 1

    deadOn = 2

    avoid = 3

state = Enum('State', ['idle', 'deadOn', 'avoid'])

### END ###


### CONSTANTS DECLATIONS ###
# coverage of sensor array
COVERAGE = 30
MAX_ANGLE_DIFF = 5



### FIELD DECLARATIONS ###

## PUBLIC ##
# public variables for speeds
forSpeed = 0
turSpeed = 0

# public position
currentPos = [0, 0, 0] # X, Y, AZ
targetPos = [0 ,0 ,0] # X, Y, AZ

#public tuple for detection ranges
sensorArray = [0, 0, 0, 0, 0, 0]
## END ##

## PRIVATE ##

# lock for the speed data.  Proably not needed
data_lock = Lock()

# control whether the main loop is currently executing
running = True

# local accessors for getting individual data
currX, currY, currAZ = currentPos
targX, targY, targAZ = targetPos


## END ##
### END ###

### FUNCTION DEFINITIONS ###

def getAngleDiff():
    return currAZ - atan2(currX - targX, currY - targY)

def turnTowards():

    # If theres a large difference in between the target and current angle, then 
    if (abs(currAZ - targAZ) > MAX_ANGLE_DIFF):

    turnSpeed = currentPos()
    return

def deadOn():
    return

def avoid():
    return

### END ###

### MAIN ###

#main loop of code
def main():
    while(running):
        match state:
            case 'idle':
                print("idling")
                wait(0.5)
            case 'deadOn':
                deadOn()
            case 'avoid':
                avoid()

### END ###