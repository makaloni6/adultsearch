import os
import sys
import codecs
import re
import textwrap
import pprint
#asinlist -- pass
def searchasin(asinlist):
	# d = sys.argv[1]
	if asinlist == None:
		asinlist = sys.argv[1]

	## asin list ##
	with open(asinlist, "r", encoding="utf-8") as f:
		asin = f.read()
	asin = asin.split("\n")

	directry_name = [
		"honeycomb1_his_1114",
		"honeycomb2_his_1114",
		"honeycomb3_his_1114",
		"monte1_his_1114",
		"monte2_his_1112",
		"huratto_his_1114",
		"saint_his_1108",
		"japan_his_1114"
	]
	for directry in directry_name:
		print("now processing "+directry+"...")
		path = "./" + directry
		files = os.listdir(path=path)

		# print(files)
		file = {}

		## search ##
		for _ in files:
			p = path + "/" + _
			with open(p,encoding="utf8", errors='ignore') as f:
			    line = f.read()
			for _1 in asin:

				if _1 in line:
					# file.append(_)
					if _ in file:
						file[_] += 1
					else:
						file[_] = 1

		with open("./category_list.csv", "a") as f:
			f.write("--------------"+directry+"--------------\n")
			for k, v in file.items():
				f.write(k+","+str(v))
				f.write("\n")

def search_adult_asin(asinlist, name):
	for idx, _ in enumerate(asinlist):
		asinlist[idx] = re.split("[/.]", _)[1]
	print(asinlist)

	asindict = {}
	def __open_list():
		directry_name = [
			"./category_search/honeycomb1_his_1114",
			"./category_search/honeycomb2_his_1114",
			"./category_search/honeycomb3_his_1114",
			"./category_search/monte1_his_1114",
			"./category_search/monte2_his_1112",
			"./category_search/huratto_his_1114",
			"./category_search/saint_his_1108",
			"./category_search/japan_his_1114"
		]

		for directry in directry_name:
			print("now processing "+directry+"...")
			path = directry
			# files = os.listdir(path=path)
			# for _ in files:
			# 	print(_)
			files = [filename for filename in os.listdir(path) if not filename.startswith('.')]
			# return
			for _ in files:
				p = path + "/" + _

				with open(p, encoding="utf8", errors='ignore') as f:
					line = f.readlines()
				# print(line[0])
				# print(line[0].split(","))
				for idx, _1 in enumerate(line):
					try:
						address, asin = _1.split(",")[19], _1.split(",")[0]
					except:
						# print(_1.split(","))
						print(p)
						print(idx)
						# break


					try:
						address = re.split("[,/.]", address)[-3]
						asindict[address] = asin
					except:
						continue
			# 	break
			# break

	__open_list()
	# asindict = sorted(asindict.items())
	asindict = sorted(asindict.items(), key=lambda x:x[0])




	with open("./result_"+name+".csv", "w") as f:
		# f.write("--------------"+directry+"--------------\n")
		for _1 in asinlist:
			for _2 in asindict:
				if _2[0] == _1:
					f.write(_2[0] + " : " + _2[1]+"\n")


if __name__ == '__main__':
	asinlist = None
	searchasin(asinlist)
