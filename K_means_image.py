# William Patrick
# 
import math 
import sys
import numpy as np
from PIL import Image
from random import randint

number_clusters = int(sys.argv[1])

# read in image data
filename = sys.argv[2]
im_original = Image.open(filename).convert("RGB")

width = im_original.size[1]
height = im_original.size[0]

#maximum "distance" between two colors is 
max_color_distance = 362.0

#minimum distance between initial centroids
min_centroid_color_distance = 45.0

labels = [-1] * (width * height)
labels_previous =  [-1] * (width * height)


# run k means until no differences in labels and labels_previous
label_check = False
centroids_randomized = False

data = np.array(im_original)
centroids = [data[0][0]] * number_clusters

#initialize centroids with no repeating values if possible
for i in range(number_clusters):
	centroids[i] = data[randint(0,width - 1)][randint(0,height - 1)]

while(centroids_randomized == False):
	centroids_randomized = True
	for i in range(number_clusters):
		for j in range(number_clusters):
			if(math.dist(centroids[i], centroids[j]) < min_centroid_color_distance and i != j):
				centroids_randomized = False
				centroids[j] = data[randint(0,width - 1)][randint(0,height - 1)]

print("old centroids")
for i in range(number_clusters):
	print(centroids[i])

while(label_check != True):
	#set the label check to true, it will be made false later if k means is not finished
	label_check = True
	
	#loop through all pixels and find nearest centroid
	for point_x in range(width):
		for point_y in range(height):
			min_distance = 362.0
			for i in range(number_clusters):
				current_distance = math.dist(data[point_x][point_y], centroids[i])
				if(current_distance < min_distance):
					labels[(point_y * width + point_x) - 1] = i
					min_distance = current_distance
	
	count = 0.0
	result = [0.0,0.0,0.0]
	#recalculate centroids
	for i in range(number_clusters):
		for point_x in range(width):
			for point_y in range(height):
				if(labels[(point_y * width + point_x) - 1] == i):
					result += data[point_x][point_y]
					count += 1.0
		if(count != 0.0):
			result[0] /= count
			result[1] /= count
			result[2] /= count
			centroids[i] = result
		count = 0.0
		result = [0.0,0.0,0.0]
	
	#run check to see if code needs to keep running k means
	for x in range((width * height) - 1):
		if(labels[x] != labels_previous[x]):
			label_check = False
				
	#update the label values for check next loop
	for x in range((width * height) - 1):
			labels_previous[x] = labels[x]
# print results
for i in range(number_clusters):
	for point_x in range(width):
		for point_y in range(height):
			if(labels[(point_y * width + point_x) - 1] == i):
				data[point_x][point_y] = centroids[i]

print("new centroids")
for i in range(number_clusters):
	print(centroids[i])
	
#write result to new file
im = Image.fromarray(data)
filename.replace(".png","")
im.save("Output/"+ filename +str(number_clusters)+"clusters.png")
