import datetime

import cv2
import imutils


class TrafficProcessor:
    def __init__(self):
        # initialize the first frame in the video stream
        self.firstFrame = None

        self.light = "Green"
        self.cnt = 0
        self.limit = 100
        self.zone1 = (100, 150)
        self.zone2 = (450, 145)
        self.vehic = []

    def getProcessedImage(self, frame):
        # frame = frame if args.get("video", None) is None else frame[1]
        text = ""
        isCar = False
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            return None

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if self.firstFrame is None:
            self.firstFrame = gray
            return None
            # return self.getProcessedImage(frame)

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(self.firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        self.cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = self.cnts[0] if imutils.is_cv2() else self.cnts[1]

        flag = {}
        # loop over the contours
        for c in self.cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            if self.zone1[0] < (x + w / 2) < self.zone2[0] and self.zone1[1] + 100 > (y + h / 2) > self.zone2[1] - 100:
                isCar = True

            if self.light == "Red" and self.zone1[0] < (x + w / 2) < self.zone2[0] and (y + h / 2) < self.zone1[1] and (
                    y + h / 2) > self.zone2[1]:
                # print("Hello")
                rcar = frame[y:y + h, x:x + w]
                rcar = cv2.resize(rcar, (0, 0), fx=4, fy=4)
                cv2.imwrite('reported_car/reported_car_' + str(self.cnt) + ".jpg", rcar)
                self.cnt += 1
                text = "<Violation>"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        if not isCar:
            self.firstFrame = gray
        # draw the text and timestamp on the frame
        if self.light == "Green":
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv2.rectangle(frame, self.zone1, self.zone2, (255, 0, 0), 2)
        cv2.putText(frame, "Signal Status: {}".format(self.light), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.putText(frame, "{}".format(text), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, color, 1)

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)
        # cv2.imshow("Gray", gray)
        # cv2.imshow("Reference Frame", self.firstFrame)
        return frame
