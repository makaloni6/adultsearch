import boto3
import json
import glob
import sys
import re
import os
import io
from tqdm import tqdm
import zipfile
import unicodedata
import logging
from pykakasi import kakasi
from distutils.dir_util import copy_tree
import searchasin
import time
from PIL import Image

#initiate kakasi
kakasi = kakasi()

kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')
conv = kakasi.getConverter()


#aws:create boto3 client, set resion
client = boto3.client('rekognition','ap-northeast-1')

#setting for logging
logger = logging.getLogger('LoggingTest')
logger.setLevel(10)
fh = logging.FileHandler('test.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)

asin_dict = {}
# return list(contains adult images ASIN)


def img_read(directy_name):
	images = glob.glob(directy_name+"/*.jpg")
	# images = [
	# 	"./honeycomb440/419x6YjQKFL._SL1000_.jpg",
	# 	"./honeycomb440/41iFJbP5A2L._SL1000_.jpg",
	# 	"./honeycomb440/31YvjfwMJnL._SL1000_.jpg",
	# 	"./honeycomb440/41OYTZQamoL._SL1000_.jpg",
	# 	"./honeycomb440/41Rp1hUKBKL._SL1000_.jpg",
	# 	"./honeycomb440/51srDuWe9UL._SL1000_.jpg",
	# 	"./honeycomb440/31XjWZ1Cx8L._SL1000_.jpg",
	# 	"./honeycomb440/31e3MwxyRpL._SL1000_.jpg",
	# 	"./honeycomb440/41jfSEfX1VL._SL1000_.jpg",
	# 	"./honeycomb440/51BmosCiuAL._SL1000_.jpg"
	# ]

	img_name, img_byte = ["" for _1 in range(len(images))], ["" for _2 in range(len(images))]

	# print(directy_name)

	print("images")
	print(len(images))
	# print(images[1:10])
	# print("img_name")
	# print(len(img_name))
	# print(images[0])
	# try:
	# 	# img = open(images[0], 'rb', encoding="utf-8")
	# 	# with open("./boardgame/61vCSEHjeSL (1).jpg", 'rb')
	# 	# img = open(images[0], 'rb', encoding="utf-8")
	# except:
	# 	print("error")
	# print(img)
	error_jpg = []
	for idx, _ in enumerate(images):
		img_name[idx] = _
		try:
			img = Image.open(_, 'r')
		except:
			continue
		# print("img")
		# print(img)
		img_resize = img.resize((int(img.width / 2), int(img.height / 2)))
		title, ext = os.path.splitext(_)
		ib = io.BytesIO()
		# img_resize.save(ib, "./resize/" + title[9:] + '_r' + ext)
		if img_resize.mode != "RGB":
			img_resize.convert("RGB")

		try:
			img_resize.save(ib, format="JPEG")
		except:
			print(img_resize.mode)
			continue
		img_byte[idx] = ib.getvalue()
		# try:
		# except:
		# 	error_jpg.append(idx)
		# if idx % 10 == 0:
		# 	time.sleep(0.2)

	# for _1, _2 in zip(img_name, img_byte):
	# 	print(_1+" : "+str(_2[1:10]))
	# print("error")
	# print(error_jpg)

	return img_name, img_byte


def access_rekognition(img_name, img_byte):
	adult_img = []
	print("start rekognition")
	print(img_name[0])
	count = 0
	for n_, b_ in zip(img_name, img_byte):
		if count == 10000:
			break

		response = client.detect_moderation_labels(
			Image = {
				'Bytes': b_
			},
			MinConfidence = 60
		)
		print("result : "+n_)
		print(response['ModerationLabels'])
		count += 1
		if not response['ModerationLabels']:
			print("here")
			continue
		elif response['ModerationLabels'][0]['Name'] == "Violence" or response['ModerationLabels'][0]['ParentName'] == "Violence":
			print("Violence")
			print(response['ModerationLabels'][0])
		else:
			adult_img.append(n_)
	print("adult_img")
	print(adult_img)
	return adult_img

if __name__ == '__main__':
	zip_name = sys.argv[1]
	shop_name = sys.argv[2]
	print("hey")
	directy_list = os.listdir("./")
	print(directy_list, shop_name)
	if shop_name not in directy_list:
		print("here")
		with zipfile.ZipFile("./"+zip_name) as zf:
			zf.extractall()

	# zip_name = zip_name[:-4]
	# print(zip_name)ls

	img_name, img_byte = img_read(shop_name)
	#
	print("len images : ", len(img_byte))
	asinlist = access_rekognition(img_name[:5], img_byte[:5])
	# print(len(asinlist))
	# # asinlist = [
	# # 	"adult/thisisadult._SL1000_.jpg",
	# # 	"adult/31MEH50474L._SL1000_.jpg",
	# # 	"adult/31BRM9kBP3L._SL1000_.jpg",
	# # 	"adult/31Qz5G-2lUL._SL1000_.jpg",
	# # 	"adult/31jqN5c6TIL._SL1000_.jpg"
	# # ]
	searchasin.search_adult_asin(asinlist, shop_name)
