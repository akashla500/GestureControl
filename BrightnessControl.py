import cv2
import math
import numpy as np
import os as brightnessControl


class BrightnessControl:

    def __init__(self):
        self.brightness = 50

    def changeBrightness(self, captureImage, landMarkerList):
        xThumb, yThumb = landMarkerList[4][1], landMarkerList[4][2]
        xIndex, yIndex = landMarkerList[8][1], landMarkerList[8][2]
        xLineCenter, yLineCenter = (xIndex + xThumb) // 2, (yIndex + yThumb) // 2
        cv2.circle(captureImage, (xThumb, yThumb), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(captureImage, (xIndex, yIndex), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(captureImage, (xThumb, yThumb), (xIndex, yIndex), (255, 0, 0), 2)
        cv2.circle(captureImage, (xLineCenter, yLineCenter), 7, (255, 0, 0), cv2.FILLED)
        lineLength = math.hypot(xIndex - xThumb, yIndex - yThumb)
        # system volume can be set with range from 0 to 100
        # finger length range from 30 to 180
        brightness = np.interp(lineLength, [30, 180], [0, 100])
        if abs(self.brightness - brightness) >= 7:
            self.brightness = brightness
            brightnessControl.system(
                'gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path '
                '/org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set '
                'org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 ' + str(
                    int(brightness)) + '>"')

    def brightnessModeCheck(self, captureImage, landMarkerList):
        if landMarkerList[9][2] > landMarkerList[12][2] and landMarkerList[13][2] < landMarkerList[16][2] and \
                landMarkerList[17][2] < landMarkerList[20][2]:
            self.changeBrightness(captureImage, landMarkerList)
