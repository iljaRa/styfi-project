import numpy as np
import cv2 as cv
from pathlib import Path
import itertools
import pickle

import os
import io
from PIL import Image
from array import array

# --- Create a list of keypoints and descriptors and save it as a 
# --- pickle file. Only called if no pickle file in the current path.
# --- This function only runs once - when the dataset is new or updated.
def compute_and_serialize_kp_and_des(dataset):
    """ Compute keypoints and descriptors for every jpg picture in dataset_path
    and save them serialized.    
    """
	
	# Create a SIFT object
    sift = cv.SIFT_create(contrastThreshold = 0.05 , edgeThreshold = 5)

	# For every image in the dataset, detect keypoints and descriptors
    results = {}
    for i, jpg in enumerate(Path(dataset).glob("*.jpg")):
        jpg = str(jpg)
        img = cv.imread(jpg,1)
        try:
            kp, des = sift.detectAndCompute(img,None)
        except:
            print(jpg)
            raise
        serialized_kp = []
        for point in kp:
            temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id)
            serialized_kp.append(temp)

        results[jpg.replace("\\","/")] = [serialized_kp,des]



    with open('kp_des_' + dataset + '.p', 'wb') as fp:
        pickle.dump(results, fp)

# --- Load keypoints and descriptors of images from the dataset
def deserialize_kp_and_des(serialized_kp_path, store):
	""" Load an image database serialized with "compute_and_serialize_kp_and_des()"
	"""
	serialized_kp_path = serialized_kp_path + store + ".p"
	with open(serialized_kp_path, 'rb') as fp:
		serialized_kp = pickle.load(fp)
	
	results = {}
	for jpg in serialized_kp:
		serialized_kp_list = serialized_kp[jpg][0]
		kp_list = [0 for x in range(len(serialized_kp_list))]
		for i, kp in enumerate(serialized_kp_list):
			kp_list[i] = cv.KeyPoint(x=kp[0][0], y=kp[0][1], _size=kp[1], _angle=kp[2],
										_response=kp[3], _octave=kp[4], _class_id=kp[5])
		results[jpg] = [kp_list,serialized_kp[jpg][1]]
	
	return results

# --- Use Computer Vision to create a sorted list of best matches
def rank(query_path, database, verbose = False):
	# Create a SIFT object
	sift = cv.SIFT_create(contrastThreshold = 0.05 , edgeThreshold = 5)
	
	query_path = str(Path(query_path))
	query_img = cv.imread(query_path,1)
	query_kp , query_des = sift.detectAndCompute(query_img,None)

	# Use the Brute Force Matcher
	bf = cv.BFMatcher()
	distances = {}
	
	print(len(database))
	
	# Iterate over the images in the database and compute their
	# distance to the input image
	for i, jpg in enumerate(database):
		try:   
			matches = bf.knnMatch(query_des ,database[jpg][1],k=2)
			matches = sorted(matches,  key = lambda x :x[0].distance)
			good = []
			db_img_kps = []
			for m,n in matches:
				if m.distance < 0.75*n.distance:
					if m.trainIdx not in db_img_kps:
						good.append(m)
						db_img_kps.append(m.trainIdx)
						
						# We use four different types of distances
						if len(good) > 0:
							avg = sum([match.distance for match in good]) / len(good)
							distances[jpg] = {"avg_distance":avg, "matches": matches, "good": good, 
											  "dist1": avg, "dist2": avg*((len(matches)-len(good))**2), 
											  "dist3": avg*((len(matches)-len(good)**2)),  
											  "dist4": avg*((len(matches)-len(good))**2)/len(good)}
		except:
			if verbose:
				print(jpg)
				
	rankings = []
	rankings.append( sorted(distances, key= lambda x:distances[x]["dist1"]))
	rankings.append( sorted(distances, key= lambda x:distances[x]["dist2"]))
	rankings.append( sorted(distances, key= lambda x:distances[x]["dist3"]))
	rankings.append( sorted(distances, key= lambda x:distances[x]["dist4"]))

	return rankings, distances

