# TardigradeTracker 
import math
import numpy as np
import cv2
import easygui
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import subprocess

import PIL.Image
import PIL.ImageTk
import PIL.ImageEnhance
from sklearn.metrics import r2_score, mean_squared_error

# TODOs
# 1) Get everything up on git and learn how to use it
# *******************************************************
# *******************************************************
# Crop, Brightness and Contrast Tool
# *******************************************************
# *******************************************************

class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

class VideoEditorGui:
    def __init__(self, vs, mc, window, debug):
        self.mc = mc
        self.window = window
        self.originalVideo = vs.originalVideo
        self.videoWidth = int(self.originalVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.videoHeight = int(self.originalVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.videoFrameCount = int(self.originalVideo.get(cv2.CAP_PROP_FRAME_COUNT))

        self.lastStartX = 0
        self.lastStartY = 0
        self.lastEndX = 0
        self.lastEndY = 0
        self.cropBox = None
        self.tempCropBox = None
        self.stop = True
        self.atFrame = 0
        self.calculatingRender = False
        self.processingVideo = False
        self.zoomedIn = False
        self.zoomButtonClicked = False

        self.canvas = ResizingCanvas(self.window, width=self.videoWidth/3, height=self.videoHeight/3)
        self.canvas.place(x=0, y=0)
        self.canvas.bind("<Button-1>", self.lClickDown)
        self.canvas.bind('<ButtonRelease-1>', self.lClickUp)
        self.canvas.bind('<B1-Motion>', self.lDrag)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.timeVar = tk.IntVar()
        self.timeSlider = tk.Scale(self.window, label="Time", from_=0, to=self.videoFrameCount-1,
                                   length=self.videoWidth/3, orient='horizontal', variable=self.timeVar, sliderlength=10)
        self.timeSlider.bind('<ButtonRelease-1>', self.timeSliderUpdate)
        self.timeSlider.bind('<B1-Motion>', self.timeSliderUpdate)
        self.timeSlider.pack()

        self.contrastSlider = tk.Scale(self.window, label="Contrast", from_=0.025, to=3, resolution=0.025,
                                       length=self.videoWidth/3, orient='horizontal', sliderlength=10)
        self.contrastSlider.bind('<ButtonRelease-1>', self.imageEditorSliderUpdates)
        self.contrastSlider.pack()
        self.contrastSlider.set(0.9)

        self.brightNessSlider = tk.Scale(self.window, label="Brightness", from_=0, to=255, resolution=0.025,
                                         length=self.videoWidth/3, orient='horizontal', sliderlength=10)
        self.brightNessSlider.bind('<ButtonRelease-1>', self.imageEditorSliderUpdates)
        self.brightNessSlider.pack()
        self.brightNessSlider.set(0)

        self.thresholdSlider = tk.Scale(self.window, label="Threshold", from_=4, to=14, resolution=1,
                                       length=self.videoWidth/3, orient='horizontal', sliderlength=10)
        self.thresholdSlider.bind('<ButtonRelease-1>', self.imageEditorSliderUpdates)
        self.thresholdSlider.pack()
        self.thresholdSlider.set(14)

        # 🔄 Curves Slider
        self.curveSlider = tk.Scale(self.window, label="Curves", from_=0.1, to=3.0, resolution=0.05,
                                    length=self.videoWidth/3, orient='horizontal', sliderlength=10)
        self.curveSlider.bind('<ButtonRelease-1>', self.imageEditorSliderUpdates)
        self.curveSlider.pack()
        self.curveSlider.set(1.0)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        self.zoomButton = tk.Button(button_frame, text="Zoom In", command=self.toggleZoom)
        self.zoomButton.pack(side=tk.LEFT, padx=5)

        self.runAlgorithmButton = tk.Button(button_frame, text="Run", command=self.stopRender)
        self.runAlgorithmButton.pack(side=tk.LEFT, padx=5)

        self.imageEditorSliderUpdates(None)
        self.greyFullBackground = self.mc.greyBackground

        self.update()
        self.window.mainloop()

        if self.processingVideo:
            self.mc.processVideo()

    def toggleZoom(self):
        if self.zoomedIn:
            self.zoomedIn = False
            self.zoomButton.config(text="Zoom In")
        else:
            if self.cropBox:
                self.zoomedIn = True
                self.zoomButtonClicked = True
                self.zoomButton.config(text="Zoom Out")
        self.render()

    def lClickDown(self, event):
        self.startX = event.x
        self.startY = event.y

    def lClickUp(self, event):
        self.tempCropBox = None
        if self.startX == event.x and self.startY == event.y:
            self.stop = not self.stop
        else:
            if abs(event.x - self.startX) > 10 and abs(event.y - self.startY) > 10:
                self.cropBox = (min(self.startX, event.x), min(self.startY, event.y),
                                max(self.startX, event.x), max(self.startY, event.y), 1)
                self.lastStartX = self.startX
                self.lastStartY = self.startY
                self.lastEndX = event.x
                self.lastEndY = event.y
                self.imageEditorSliderUpdates(None)
            elif self.stop:
                self.render()

    def lDrag(self, event):
        self.tempCropBox = (self.startX, self.startY, event.x, event.y, 1)
        if self.stop:
            self.render()

    def timeSliderUpdate(self, _):
        self.atFrame = self.timeSlider.get()
        self.render()

    def imageEditorSliderUpdates(self, _):
        self.calculatingRender = True
        contrastDiff = self.contrastSlider.get()
        brightnessDiff = self.brightNessSlider.get()
        thresholdSetting = self.thresholdSlider.get()
        curveGamma = self.curveSlider.get()
        if self.cropBox:
            (x1, y1, x2, y2, _) = self.cropBox
            scale_x = self.videoWidth / self.canvas.width
            scale_y = self.videoHeight / self.canvas.height
            finalCropBox = (int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y))
        else:
            finalCropBox = None
        self.mc.processBackground(thresholdSetting, brightnessDiff, contrastDiff, finalCropBox, curveGamma)
        self.calculatingRender = False
        if self.stop:
            self.render()
            
    
    def render(self):
        if self.calculatingRender:
            return

        self.originalVideo.set(cv2.CAP_PROP_POS_FRAMES, self.atFrame)
        ret, frame = self.originalVideo.read()
        if not ret:
            return

        (annotated, _, _, _, _, _, _) = self.mc.processFrame(frame, 0)
        rgb_image = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        self.renderVideoWidth = int(self.canvas.width)
        self.renderVideoHeight = int(self.videoHeight * self.canvas.width / self.videoWidth)
        if self.renderVideoHeight > int(self.canvas.height):
            self.renderVideoHeight = int(self.canvas.height)
            self.renderVideoWidth = int(self.videoWidth * int(self.canvas.height) / self.videoHeight)

        self.timeSlider.set(self.atFrame)
        self.canvas.delete("all")

        if self.zoomedIn and self.cropBox and self.zoomButtonClicked:
            (x1, y1, x2, y2, _) = self.cropBox
            width, height = abs(x2 - x1), abs(y2 - y1)
            magnification = min(self.renderVideoWidth/width, self.renderVideoHeight/height)
            newWidth, newHeight = width*magnification, height*magnification

            resized_image = cv2.resize(rgb_image, (int(newWidth), int(newHeight)), interpolation=cv2.INTER_AREA)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resized_image))
            self.canvas.create_image((self.renderVideoWidth-newWidth)/2, (self.renderVideoHeight-newHeight)/2,
                                     image=self.photo, anchor=tk.NW)

        elif self.cropBox:
            (x1, y1, x2, y2, _) = self.cropBox
            resized_image = cv2.resize(rgb_image, (abs(x1 - x2), abs(y1 - y2)), interpolation=cv2.INTER_AREA)
            resized_bg = cv2.resize(self.greyFullBackground, (self.renderVideoWidth, self.renderVideoHeight), interpolation=cv2.INTER_AREA)

            self.bg = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resized_bg))
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resized_image))
            self.canvas.create_image(0, 0, image=self.bg, anchor=tk.NW)
            self.canvas.create_image(min(x2, x1), min(y1, y2), image=self.photo, anchor=tk.NW)
            self.canvas.create_line((x2, y1), (x1, y1))
            self.canvas.create_line((x1, y1), (x1, y2))
            self.canvas.create_line((x1, y2), (x2, y2))
            self.canvas.create_line((x2, y2), (x2, y1))

        else:
            resized_image = cv2.resize(rgb_image, (self.renderVideoWidth, self.renderVideoHeight), interpolation=cv2.INTER_AREA)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resized_image))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.tempCropBox:
            (x1, y1, x2, y2, _) = self.tempCropBox
            self.canvas.create_line((max(x1, x2), min(y1, y2)), (min(x1, x2), min(y1, y2)), dash=(5, 2))
            self.canvas.create_line((min(x1, x2), min(y1, y2)), (min(x1, x2), max(y1, y2)), dash=(5, 2))
            self.canvas.create_line((min(x1, x2), max(y1, y2)), (max(x1, x2), max(y1, y2)), dash=(5, 2))
            self.canvas.create_line((max(x1, x2), max(y1, y2)), (max(x1, x2), min(y1, y2)), dash=(5, 2))

    def stopRender(self):
        self.calculatingRender = True
        self.processingVideo = True
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.iconify()
        self.window.destroy()

    def update(self):
        if self.calculatingRender:
            return

        if not self.stop:
            self.atFrame += 180
            if self.atFrame >= self.videoFrameCount:
                self.atFrame = 0
            self.render()

        self.window.after(15, self.update)


# *******************************************************
# *******************************************************
# Video Selector Tool
# *******************************************************
# *******************************************************


class VideoSelector:
    def __init__(self, debug):
        self.is_windows = sys.platform.startswith('win')

    def chooseFile(self):
        # import matplotlib.pyplot as plt
        # You can use plt.imshow(image) and plt.show() to visualize each step

        if self.is_windows:
            self.inputVideoLocation = easygui.fileopenbox().replace('/', '\\')
        else:
            self.inputVideoLocation = easygui.fileopenbox(filetypes=['*.mp4'])

        self.tempOutputVideoLocation = self.inputVideoLocation + 'adjusted_input.mp4'
        self.outputVideoLocation = self.inputVideoLocation
        self.outputArrayLocation = self.inputVideoLocation + '_output.csv'
        self.readVideo()

    def resetVideo(self):
        self.originalVideo.set(cv2.CAP_PROP_POS_FRAMES, 1)

    def readVideo(self):
        self.originalVideo = cv2.VideoCapture(self.inputVideoLocation)

    def releaseVideo(self):
        self.originalVideo.release()


# *******************************************************
# *******************************************************
# Main Calculator Tool
# *******************************************************
# *******************************************************

class MainCalculator:
    def __init__(self, vs, debug, minContourArea=500, maxContourArea=5000):
        self.outputVideoLocation = vs.outputVideoLocation
        self.outputArrayLocation = vs.outputArrayLocation
        self.originalVideo = vs.originalVideo
        self.prevContour = None
        self.prevCentroid = None
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.eye(2, 4, dtype=np.float32)
        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                                [0, 1, 0, 1],
                                                [0, 0, 1, 0],
                                                [0, 0, 0, 1]], dtype=np.float32)
        self.kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 1e-2
        self.kalman.measurementNoiseCov = np.eye(2, dtype=np.float32) * 1e-1
        self.kalman_initialized = False


        self.debug = debug
        self.head = [0, 0]
        self.tail = [0, 0]

        self.minContourArea = minContourArea
        self.maxContourArea = maxContourArea

    def processBackground(self, thresholdSetting, brightnessDiff, contrastDiff, cropBox, curveGamma):
        vs.resetVideo()
        self.videoWidth = int(self.originalVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.videoHeight = int(self.originalVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.thresholdSetting = thresholdSetting
        self.brightnessDiff = brightnessDiff
        self.contrastDiff = contrastDiff
        self.cropBox = cropBox

        randomFrames = self.originalVideo.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=30)
        frames = []

        for frameId in randomFrames:
            self.originalVideo.set(cv2.CAP_PROP_POS_FRAMES, frameId)
            ret, frame = self.originalVideo.read()
            if ret:
                if self.cropBox:
                    (x1, y1, x2, y2) = self.cropBox
                    frame = frame[y1:y2, x1:x2]

                if brightnessDiff != 0 or contrastDiff != 1:
                    frame = cv2.addWeighted(frame, contrastDiff, frame, 0, brightnessDiff)

                if curveGamma != 1.0:
                    invGamma = 1.0 / curveGamma
                    table = np.array([(i / 255.0) ** invGamma * 255 for i in np.arange(256)]).astype("uint8")
                    frame = cv2.LUT(frame, table)

                frames.append(frame)

        self.medianFrame = np.max(frames, axis=0).astype(dtype=np.uint8)
        self.greyBackground = cv2.cvtColor(self.medianFrame, cv2.COLOR_BGR2GRAY)

        if self.debug:
            cv2.imwrite(self.outputVideoLocation + "_greyBackground.jpg", self.greyBackground)
            cv2.imwrite(self.outputVideoLocation + "_medianFrame.jpg", self.medianFrame)

    def calculate_line_length(self, x_values, y_values):
        return sum(math.hypot(x_values[i] - x_values[i-1], y_values[i] - y_values[i-1])
                   for i in range(1, len(x_values)))

    def count_points_near_model(self, x, y, model, distance):
        y_pred = np.polyval(model, x)
        distances = np.abs(y - y_pred)
        return np.count_nonzero(distances <= distance)

    def contour_to_arrays_and_curve(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        mask = np.zeros((h, w), dtype=np.uint8)
        shifted_contour = contour - (x, y)
        cv2.drawContours(mask, [shifted_contour], 0, (255), -1)
        y_coords, x_coords = np.where(mask == 255)
        x_coords += x
        y_coords += y

        curve_coeffs_1 = np.polyfit(x_coords, y_coords, 1)
        curve_coeffs_2 = np.polyfit(x_coords, y_coords, 2)
        flipped_curve_coeffs_1 = np.polyfit(y_coords, x_coords, 1)
        flipped_curve_coeffs_2 = np.polyfit(y_coords, x_coords, 2)

        curve_x = np.linspace(x_coords.min(), x_coords.max(), 100)
        flipped_curve_y = np.linspace(y_coords.min(), y_coords.max(), 100)
        curve_y_1 = np.polyval(curve_coeffs_1, curve_x)
        curve_y_2 = np.polyval(curve_coeffs_2, curve_x)
        flipped_curve_x_1 = np.polyval(flipped_curve_coeffs_1, flipped_curve_y)
        flipped_curve_x_2 = np.polyval(flipped_curve_coeffs_2, flipped_curve_y)

        curve_models = [
            ("xy", 1, curve_x, curve_y_1, curve_coeffs_1, self.count_points_near_model(x_coords, y_coords, curve_coeffs_1, 3)),
            ("xy", 2, curve_x, curve_y_2, curve_coeffs_2, self.count_points_near_model(x_coords, y_coords, curve_coeffs_2, 3)),
            ("yx", 1, flipped_curve_x_1, flipped_curve_y, flipped_curve_coeffs_1, self.count_points_near_model(y_coords, x_coords, flipped_curve_coeffs_1, 3)),
            ("yx", 2, flipped_curve_x_2, flipped_curve_y, flipped_curve_coeffs_2, self.count_points_near_model(y_coords, x_coords, flipped_curve_coeffs_2, 3))
        ]

        best_model = max(curve_models, key=lambda m: m[5])
        best_x, best_y = best_model[2], best_model[3]
        return best_x, best_y, self.calculate_line_length(best_x, best_y), 0

    def processFrame(self, frame, frameId):
        if self.cropBox:
            (x1, y1, x2, y2) = self.cropBox
            frame = frame[y1:y2, x1:x2]

        if self.brightnessDiff != 0 or self.contrastDiff != 1:
            frame = cv2.addWeighted(frame, self.contrastDiff, frame, 0, self.brightnessDiff)

        greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dframe = cv2.absdiff(greyFrame, self.greyBackground)
        _, tframe = cv2.threshold(dframe, self.thresholdSetting, 255, cv2.THRESH_BINARY)

        cnts, _ = cv2.findContours(tframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_cnts = [c for c in cnts if self.minContourArea <= cv2.contourArea(c) <= self.maxContourArea]

        if not valid_cnts:
            self.prevContour = None
            self.prevCentroid = None
            return frame, 0, 0, (0, 0), self.head, self.tail, 0

        def contour_centroid(cnt):
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                return None
            return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if self.prevCentroid:
            def cost(cnt):
                c = contour_centroid(cnt)
                if c is None:
                    return float('inf')
                return math.hypot(c[0] - self.prevCentroid[0], c[1] - self.prevCentroid[1])
            cnt = min(valid_cnts, key=cost)
        else:
            cnt = max(valid_cnts, key=cv2.contourArea)

        self.prevContour = cnt
        centroid = contour_centroid(cnt)
        self.prevCentroid = centroid

        if centroid:
            cx, cy = centroid
            measured = np.array([[np.float32(cx)], [np.float32(cy)]])
            
            if not hasattr(self, "kalman_initialized") or not self.kalman_initialized:
                self.kalman.statePre = np.array([[cx], [cy], [0], [0]], dtype=np.float32)
                self.kalman.statePost = self.kalman.statePre.copy()
                self.kalman_initialized = True

            predicted = self.kalman.predict()
            corrected = self.kalman.correct(measured)

            smoothed_cx = float(corrected[0])
            smoothed_cy = float(corrected[1])

            cv2.circle(frame, (int(smoothed_cx), int(smoothed_cy)), 5, (0, 255, 0), -1)

        annotated = frame.copy()
        x, y, w, h = cv2.boundingRect(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(annotated, [cnt], 0, (0, 0, 255), 1)

        curve_x, curve_y, curve_length, curve_angle = self.contour_to_arrays_and_curve(cnt)
        curve_points = np.column_stack((curve_x.astype(int), curve_y.astype(int)))
        cv2.polylines(annotated, [curve_points], False, (255), thickness=2)

        end_1 = curve_points[0]
        end_2 = curve_points[-1]
        distance_to_head = math.hypot(end_1[0] - self.head[0], end_1[1] - self.head[1])
        distance_to_tail = math.hypot(end_1[0] - self.tail[0], end_1[1] - self.tail[1])

        if distance_to_head < distance_to_tail:
            self.head = end_1
            self.tail = end_2
        else:
            self.tail = end_1
            self.head = end_2

        center, (width, height), angle = rect
        tardigradeArea = cv2.contourArea(cnt)
        tardigradeLength = max(width, height)

        if self.debug and frameId % 99 == 0:
            cv2.imwrite(self.outputVideoLocation + f"{frameId}_greyFrame.jpg", greyFrame)
            cv2.imwrite(self.outputVideoLocation + f"{frameId}_dFrame.jpg", dframe)
            cv2.imwrite(self.outputVideoLocation + f"{frameId}_tFrame.jpg", tframe)
            cv2.imwrite(self.outputVideoLocation + f"{frameId}_annotated.jpg", annotated)

        return annotated, tardigradeLength, tardigradeArea, center, self.head, self.tail, curve_length


    def processVideo(self):
        if self.cropBox:
            (x1, y1, x2, y2) = self.cropBox
            self.videoWidth = abs(x1 - x2)
            self.videoHeight = abs(y1 - y2)

        videoOut = cv2.VideoWriter(self.outputVideoLocation + "_output.mp4",
                                   cv2.VideoWriter_fourcc(*"mp4v"), 30, (self.videoWidth, self.videoHeight))

        vs.resetVideo()
        imgStack = int(self.originalVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        dataOutput = [[-1] * 11 for _ in range(imgStack)]

        frameId = 0
        frameCount = self.originalVideo.get(cv2.CAP_PROP_FRAME_COUNT)
        while True:
            ret, frame = self.originalVideo.read()
            print("Running algorithm on frame", frameId, "of", frameCount, "frames. ~", int((frameId/frameCount)*100), "%")

            if not ret or frameId > frameCount:
                print("Annotated a total of", frameId, "frames...")
                break

            annotated, tardigradeLength, tardigradeArea, center, head, tail, curve_length = self.processFrame(frame, frameId)
            centerx, centery = center
            dataOutput[frameId] = [
                frameId, frameId / 30, centerx, centery,
                tardigradeLength, tardigradeArea,
                int(head[0]), int(head[1]), int(tail[0]), int(tail[1]), curve_length
            ]

            videoOut.write(annotated)
            frameId += 1

        self.originalVideo.release()
        videoOut.release()

        np.savetxt(self.outputArrayLocation, np.array(dataOutput), fmt=[
            '%d', '%.3f', '%.3f', '%.3f', '%.3f', '%.3f',
            '%.3f', '%.3f', '%.3f', '%.3f', '%.3f'
        ], delimiter=',', header="frame,second,centerx,centery,length,area,headx,heady,tailx,taily,curve_length")

        subprocess.run(['python', "/Users/mollykirk/Desktop/TardigradeTraker/TrajectoryTracker.py", self.outputArrayLocation])

debug = False
window = tk.Tk()
window.title('Tardigrades!')
vs = VideoSelector(debug)
vs.chooseFile()
mc = MainCalculator(vs, debug)
vg = VideoEditorGui(vs, mc, window, debug)

# Play sound
os.system("afplay /System/Library/Sounds/Ping.aiff")