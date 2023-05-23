from threading import Lock

class OAS_Data:

    contro_data = []
    autono_data = []
    obstacle_detection = []

    def __init__(self):
            self.contro_data = [0,0]
            self.autono_data = [0,0,0,0,0,0]
            self.obstac_data = [0,0,0]
        
            contro_lock = Lock()
            autono_lock = Lock()
            obstac_lock = Lock()

    def getControlData(self):
        with self.contro_lock:
            return self.contro_data
        
    def setControlData(self,_contro_data):
        with self.contro_lock:
            self.contro_data = _contro_data

    def getAutonomousData(self):
        with self.autono_lock:
            return self.autono_data
        
    def setAutonomousData(self,_autono_data):
        with self.autono_lock:
            self.autono_data = _autono_data

    def getDetectionData(self):
        with self.obstac_lock:
            return self.autono_lock
        
    def setDetecctionData(self,_obstac_data):
        with self.obstac_lock:
            self.obstac_data = _obstac_data
