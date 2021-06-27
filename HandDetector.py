import cv2
import mediapipe
import time


class HandDetector:
    # Time initializations
    currentTime = 0
    previousTime = 0
    processed_hands = None

    def __init__(self, staticMode=False, maxHands=1, detectionConfidence=0.5, trackingConfidence=0.5):
        self.staticMode = staticMode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence
        # Mediapipe hand initializations
        self.mediaPipeHandPoints = mediapipe.solutions.drawing_utils
        self.mediaPipeHands = mediapipe.solutions.hands
        self.hands = self.mediaPipeHands.Hands(self.staticMode, self.maxHands, self.detectionConfidence,
                                               self.trackingConfidence)

    def findHands(self, captureImage, draw=True):
        captureImageRGB = cv2.cvtColor(captureImage, cv2.COLOR_BGR2RGB)
        self.processed_hands = self.hands.process(captureImageRGB)
        if self.processed_hands.multi_hand_landmarks:
            for processed_hand in self.processed_hands.multi_hand_landmarks:
                if draw:
                    self.mediaPipeHandPoints.draw_landmarks(captureImage, processed_hand,
                                                            self.mediaPipeHands.HAND_CONNECTIONS)
        return captureImage

    def findPosition(self, captureImage, indexNumber=0, draw=True):
        landmarkList = []
        if self.processed_hands.multi_hand_landmarks:
            processedHand = self.processed_hands.multi_hand_landmarks[indexNumber]
            for indexNumber, landmark in enumerate(processedHand.landmark):
                height, width, center = captureImage.shape
                xPixel, yPixel = int(landmark.x * width), int(landmark.y * height)
                landmarkList.append([indexNumber, xPixel, yPixel])
                if draw:
                    cv2.circle(captureImage, (xPixel, yPixel), 7, (255, 0, 0), cv2.FILLED)
        return landmarkList

    def showFramePerSecond(self, captureImage):
        self.currentTime = time.time()
        framesPerSecond = 1 / (self.currentTime - self.previousTime)
        self.previousTime = self.currentTime
        cv2.putText(captureImage, "FPS : " + str(int(framesPerSecond)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 2)
