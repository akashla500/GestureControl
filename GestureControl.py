import cv2
import HandDetector as detector
import VolumeControl
import BrightnessControl


def main():
    # start video capture
    captureVideo = cv2.VideoCapture(0)
    handDetector = detector.HandDetector(detectionConfidence=0.8)
    volumeControl = VolumeControl.VolumeControl()
    brightnessControl = BrightnessControl.BrightnessControl()
    while True:
        captureStatus, captureImage = captureVideo.read()
        captureImage = handDetector.findHands(captureImage)
        landMarkerList = handDetector.findPosition(captureImage)
        if len(landMarkerList) > 0:
            brightnessControl.brightnessModeCheck(captureImage, landMarkerList)
            volumeControl.volumeModeCheck(captureImage, landMarkerList)
        handDetector.showFramePerSecond(captureImage)
        cv2.imshow("Image", captureImage)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()
