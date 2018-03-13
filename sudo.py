import cv2
import numpy as np 
import time

#global variables
kernel_size = 3
threshold_min = 30
CV_PI = 3.1415926535897932384626433832795

def compute():
	cv2.namedWindow("Sudoku Solver")
	stream = 'http://192.168.0.2:8080/video'

	capture = cv2.VideoCapture(stream)
	if capture.isOpened():
		rval, frame = capture.read() #edgeCase
	else:
		rval = false

	while rval:

		#image preprocessing
		_init = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert rgb to gray
		_init = cv2.blur(_init, (3,3)) #convolve image with low-pass filter kernel for removing noises. Here kernel is 3x3
		edges = cv2.Canny(_init, threshold_min, threshold_min*2, kernel_size) #Canny Edge Detection

		'''
		Canny Edge Detection Algorithm works in three phases:
		
		1. Finding Intensity of Gradient--
			$ Smoothened image is filtered with Sobel Kernel in both horizontal and vertical direction.
			$ We get Gx as derivative in x-direction and Gy as derivative in y-direction
			$ From Gx and Gy we get edge gradient as G = Sqr_Root( (Gx)^2 + (Gy)^2 )
			$ Also, we can obtain direction of each pixel as, Angle(Theta) = atan(Gy/Gx)

		2. Non-Maximum Suppression--
			$ Remove any unwanted pixels which don't consitute the edge.
			$ For each edge, we obtain gradient (i.e. its normal) and for every pixel 'p' on normal,
				$$ If 'p' forms the local maximum in neighborhood in direction of gradient, keep the pixel.
				   Else, discard (suppress to 0)

		3. Hysteresis Thresholding--
			$ Find which edge do qualify for hypothesis of strong edge.
			$ Two threshold values: minVal and maxVal
			$ Definition of "strong-edge": Any edges with intensity gradient more than maxVal are sure to be edges and those below minVal are sure to be non-edges, so discarded. 
											Those who lie between these two thresholds are classified edges or non-edges based on their connectivity. 
											If they are connected to "sure-edge" pixels, they are considered to be part of edges. Otherwise, they are also discarded.

		Important ComputerPhile Links:
			$ Finding the Edges (Sobel Operator) - https://www.youtube.com/watch?v=uihBwtPIBxM
			$ Canny Edge Detector - https://www.youtube.com/watch?v=sRFM5IEqR2w 
		'''


		lines = cv2.HoughLines(edges, 2, CV_PI/180, 300, 0, 0)

		'''
		cv2.HoughLinesP(image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]]) → lines
    	Parameters:	
	        image – 8-bit, single-channel binary source image. The image may be modified by the function.
	        rho – Distance resolution of the accumulator in pixels.
	        theta – Angle resolution of the accumulator in radians.
	        threshold – Accumulator threshold parameter.
	        minLineLength – Minimum line length. Line segments shorter than that are rejected.
	        maxLineGap – Maximum allowed gap between points on the same line to link them.
		
		returns an array of (ρ,θ) values. ρ is measured in pixels and θ is measured in radians.
	    Links:
			https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html
			https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/	
		'''

		if lines is not None:
			lines = lines[0]
			print(lines)
			lines = sorted(lines, key=lambda line:line[0])

			#define position of horizontal line and vertical line
			pos_horizontal = 0
			pos_vertical = 0

			for rho, theta in lines:
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a*rho
				y0 = b*rho

				x1 = int(x0 + 10000*(-b))
				y1 = int(y0 + 10000*(a))
				x2 = int(x0 - 10000*(-b))
				y2 = int(y0 - 10000*(a))

				#if b > 0.5, angle must be greater than 45 degree, hence line is vertical.

				if b > 0.5:
					if rho-pos_horizontal > 10:
						pos_horizontal = rho
						cv2.line(frame, (x1,y1), (x2,y2), (0,0,255), 2)
					elif rho-pos_vertical > 10:
						pos_vertical = rho
						cv2.line(frame, (x1,y1), (x2,y2), (0,0,255), 2)

		cv2.imshow("Sudoku Solver", frame)
		rval, frame = capture.read()
		key = cv2.waitKey(20) & 0xFF
		if key == ord('q'):
			break

	capture.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	time.sleep(5)
	compute()