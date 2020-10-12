import kp_des_sift as kds
from pathlib import Path
import sys
import os

# --- LOAD OR CREATE THE KEYPOINTS DATASET (it can take some minutes)
store="hm"
if not Path("kp_des_dataset_"+ store + ".p").exists():
    kds.compute_and_serialize_kp_and_des("dataset_"+ store)
    
database = kds.deserialize_kp_and_des("kp_des_dataset_", store)

# --- APPLY COMPUTER VISION - SIFT, with OpenCV, to find fashion 
# --- items from the dataset matching the ones on the input image
input_img = sys.argv[1]
rankings, distances = kds.rank(input_img,database)

# --- SELECT THE BEST THREE
show_rankings = rankings[3]

# --- EXPORT THE PRODUCT IDs OF THE THREE BEST MATCHES
products = [];
result_count = 0
output_file = sys.argv[2]

with open(output_file, "w+") as results_file:
	for item in show_rankings:
		item = item.split("/")[1]
		if ".jpg" in item:
			item = item.replace(".jpg","")
		item_array = item.split("_")[:-1]
		product_id = '_'.join([str(elem) for elem in item_array])
		if product_id not in products:
			products.append(product_id)
			results_file.write("%s\n" % product_id)
			result_count +=1
		if result_count>2:
			break
		
		
	
