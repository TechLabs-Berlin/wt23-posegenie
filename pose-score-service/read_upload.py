import cv2

# Video Reader
class readUpload:
    def __init__(self, filename, pose):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)
        self.pose = pose
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.timestamps = [self.cap.get(cv2.CAP_PROP_POS_MSEC)]
        self.calc_timestamps = [0.0]
    
    def read_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret is False or frame is None:
                return None
        else:
            return None
        return frame
    
    def recolor_RGB(self):
        frame = self.read_frame()
        if frame is None: 
            return(None, "No Frame Detected")
        else:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.pose.process(frame)
            return image, results
        
    def get_frame_width(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_frame_height(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def get_video_fps(self):
        return self.cap.get(cv2.CAP_PROP_FPS)
    
    def get_timestamps(self):
        return self.cap.get(cv2.CAP_PROP_POS_MSEC)