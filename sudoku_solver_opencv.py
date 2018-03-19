#sudo -_-

import cv2
import operator
import numpy as np
from matplotlib import pyplot as plt

def show_image(img):
	cv2.imshow('image', img)  #Display the image
	cv2.waitKey(0)  #Wait for any key to be pressed (with the image window active)
	cv2.destroyAllWindows() #Close all windows

def plot_many_images(images, titles, rows=1, columns=2):
	for i, image in enumerate(images):
		plt.subplot(rows, columns, i+1)
		plt.imshow(image, 'gray')
		plt.title(titles[i])
		plt.xticks([]), plt.yticks([])  # Hide tick marks
	plt.show()

def display_points(in_img, points, radius=5, colour=(0, 0, 255)):

	img = in_img.copy()
	if len(colour) == 3:
		if len(img.shape) == 2:
			img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		elif img.shape[2] == 1:
			img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	for point in points:
		img = cv2.circle(img, tuple(int(x) for x in point), radius, colour, -1)
	show_image(img)
	return img

def display_rects(in_img, rects, colour=255):

	img = in_img.copy()
	for rect in rects:
		img = cv2.rectangle(img, tuple(int(x) for x in rect[0]), tuple(int(x) for x in rect[1]), colour)
	show_image(img)
	#return img

#Blur image to reduce noise obtained in thresholding algorithm
#Binary Thresholding - makes split of either 0/1 on basis of threshold measured from entire image
#Adaptive Thresholding - calculates threshold for each pixel based on mean value of surrounding pixels
#Dilate image to increase thickness of lines
def preprocess_img(img, skip_dilate = False):

	#Kernel size: +ve, odd, square
	preprocess  = cv2.GaussianBlur(img.copy(), (9, 9), 0)

	#cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, constant(c))
	#the threshold value T(x, y) is a weighted sum (cross-correlation with a Gaussian window) of {blockSize} x {blockSize} neighborhood of (x, y) minus C
	preprocess = cv2.adaptiveThreshold(preprocess, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

	#we need grid edges, hence,
	#invert colors: gridlines will have non-zero pixels
	preprocess = cv2.bitwise_not(preprocess, preprocess)

	if not skip_dilate:
		kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]])
		preprocess = cv2.dilate(preprocess, kernel)

	return preprocess



def find_external_contours(processed_image):

	#findContours: boundaries of shapes having same intensity
	#CHAIN_APPROX_SIMPLE - stores only minimal information of points to describe contour
    #-> RETR_EXTERNAL gives "outer" contours, so if you have (say) one contour enclosing another (like concentric circles), only the outermost is given.
    #-> RETR_LIST gives all the contours and doesn't even bother calculating the hierarchy -- good if you only want the contours and don't care whether one is nested inside another.
    #-> RETR_CCOMP gives contours and organises them into outer and inner contours. Every contour is either the outline of an object, or the outline of an object inside another object (i.e. hole). The hierarchy is adjusted accordingly. This can be useful if (say) you want to find all holes.
    #-> RETR_TREE calculates the full hierarchy of the contours. So you can say that object1 is nested 4 levels deep within object2 and object3 is also nested 4 levels deep.

	new_img, ext_contours, hier = cv2.findContours(processed_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	new_img, contours, hier = cv2.findContours(processed_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)
	show_image(processed_image)

	#Draw all contours on image in 2px red lines
	all_contours = cv2.drawContours(processed_image.copy(), contours, -1, (255, 0, 0,), 2)
	external_contours = cv2.drawContours(processed_image.copy(), ext_contours, -1, (255, 0 ,0 ), 2)

	#Plot images
	plot_many_images([all_contours, external_contours], ['All contours', 'External Only'])
	


def get_corners_of_largest_poly(img):

	#cv2.ContourArea(): Finds area of outermost polygon(largest feature) in img.
	#Ramer Doughlas Peucker algorithm: Approximate no of sides of shape(filter rectangle objects only).

	#Top Left: Smallest x and smallest y co-ordinate [minimise](x+y)
	#Top Right: Largest x and smallest y co-ordinate [maximise](x-y)
	#Bottom Left: Largest x and largest y co-ordinate [maximise](x+y)
	#Bottom Right: Smallest x and largest y co-ordinate [minimise](x-y)

	_, contours, h = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=cv2.contourArea, reverse=True) #Sort by area, descending

	#for ele in contours:
	#	print(ele)

	polygon = contours[0] #get largest contour
	print(polygon)

	#operator.itemgetter - get index of point
	bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
	top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
	bottom_left, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
	top_right, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))

	print("\n"+str(bottom_right)+" "+str(bottom_left)+" "+str(top_right)+" "+str(top_left))

	return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]


def infer_sudoku_puzzle(image, crop_rectangle):
	#wrapPerspective: implementation of perspective transform equation.
	#https://docs.opencv.org/3.1.0/da/d6e/tutorial_py_geometric_transformations.html
	
	#X = (ax + by + c) / (gx + hy + 1) 	X, Y -> new coords || x,y -> old coords || a..h -> constants
	#Y = (dx + ey + f) / (gx + hy + 1)
	#Map four coords from og img to new locations in new img
	#https://wp.optics.arizona.edu/visualopticslab/wp-content/uploads/sites/52/2016/08/Lectures6_7.pdf

	img = image
	crop_rect = crop_rectangle
	
	def distance_between(a, b): #scalar distance between a and b
		#sqrt(x^2 + y^2)      where (x -> ====) and (y -> ++++)
		return np.sqrt( ((b[0] - a[0]) **2) + ((b[1] - a[1]) **2) )
		#			     ============          ++++++++++++
		#a = p2[0] - p1[0]
		#b = p2[1] - p1[1]
		#return np.sqrt((a ** 2) + (b ** 2))


	def crop_img(): #crops rectangular portion from image and wraps it into a square of similar size
		top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]
		
		source_rect = np.array(np.array([top_left, bottom_left, bottom_right, top_right], dtype='float32')) #float for perspective transformation

		#get longest side in rectangle
	    # ______
		#|      |
		#|______|
		#
		side = max([
			distance_between(bottom_right, top_right), 
			distance_between(top_left, bottom_left),
			distance_between(bottom_right, bottom_left),
			distance_between(top_left, top_right)
			])

		dest_square = np.array([[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')

		#Skew the image by comparing 4 before and after points -- return matrix 
		m = cv2.getPerspectiveTransform(source_rect, dest_square)

		#Perspective Transformation on original image
		return cv2.warpPerspective(img, m, (int(side), int(side)))

	return crop_img()


def infer_grid(img): #infer 81 cells from image
	squares = []
	side = img.shape[:1]

	side = side[0] / 9

	for i in range(9):  #get each box and append it to squares -- 9 rows, 9 cols
		for j in range(9):
			p1 = (i*side, j*side) #top left corner of box
			p2 = ((i+1)*side, (j+1)*side) #bottom right corner of box
			squares.append((p1, p2))
	return squares


def main():
	img = cv2.imread('images/sudo-2.jpg', cv2.IMREAD_GRAYSCALE)
	processed_sudoku = preprocess_img(img)

	find_external_contours(processed_sudoku)
	corners_of_sudoku = get_corners_of_largest_poly(processed_sudoku)
	display_points(processed_sudoku, corners_of_sudoku)
	cropped_sudoku = infer_sudoku_puzzle(img, corners_of_sudoku)
	show_image(cropped_sudoku)
	squares_on_sudoku = infer_grid(cropped_sudoku)
	display_rects(cropped_sudoku, squares_on_sudoku)


if __name__ == '__main__':
	main()