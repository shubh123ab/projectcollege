from keras.models import load_model
import os 
import numpy as np
import cv2 
from PIL import Image
import zipfile 

WIDTH = 224
HEIGHT =224


def predict(img, WIDTH = WIDTH, HEIGHT = HEIGHT):

	model_path = 'model.pickle'
	if not os.path.exists(model_path):
		raise FileNotFoundError('Model not found')

	model = load_model(model_path)
	
	# data = cv2.imread(os.path.join(cwd , 'test_image.png'), 0 )
	data = cv2.imread('demo.jpg', 0 )
	# data = cv2.imread(str(img.read()), 0 )
    
	# data = cv2.imdecode((np.fromstring(img.read(), np.uint8)).encode(encoding='UTF-8'), cv2.IMREAD_UNCHANGED)
	img = cv2.resize(data , (WIDTH,HEIGHT))
	x_test = [img]
	x_test = np.asarray(x_test)
	x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
	
	prediction = model.predict(x_test)
	data = []

	labels = ['covid','pneumonia', 'normal']
	for pred in prediction:
		temp = {}
		value_list = list(pred)
		for ind , val in enumerate(value_list):
			temp[labels[ind]] = float(val)

		max_index = value_list.index(max(value_list))
		report = labels[max_index]
		data.append({"health_condition": report,"values":temp})

	return data[0]