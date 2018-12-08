from Database import Database
from processor.TrafficProcessor import TrafficProcessor
from processor.violation_detection import DirectionViolationDetection


class MainProcessor:

    def __init__(self, camera_id):
        self.cam_id = camera_id
        self.cam_violation_count, self.cam_location, self.cam_feed = Database.getInstance().getCamDetails(camera_id)

        if camera_id == 'cam_01' or camera_id == 'cam_03':
            self.processor = TrafficProcessor()
            self.processor.zone1 = (100, 150)
            self.processor.zone2 = (450, 145)
            self.processor.thres = 30

        elif camera_id == 'cam_02':
            self.processor = TrafficProcessor()
            self.processor.zone1 = (100, 150)
            self.processor.zone2 = (450, 145)
            self.processor.thres = 6
            self.processor.dynamic = True

        elif camera_id == 'cam_04':
            self.processor = DirectionViolationDetection(self.cam_feed)

    def getProcessedImage(self, frame=None, cap=None):
        if self.cam_id in ['cam_01', 'cam_02', 'cam_03']:
            dicti = self.processor.cross_violation(frame)

        elif self.cam_id == 'cam_04':
            dicti = self.processor.feedCap(frame)

        return dicti

    def setLight(self, color):
        self.processor.light = color

    def getLight(self):
        return self.processor.light