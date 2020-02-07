from PIL import Image
import os
import glob
import argparse
import numpy as np


parser.add_argument("--paths", help="write a list of image paths, i.e. ['./img1', './img2']", type=list, default = ['.'])

args = parser.parse_args()

paths=args.paths


def getallpaths(listofdirs):
	all_paths = []
	for path in listofdirs:
		all_paths += [ os.path.join(path, i) for i in os.listdir(path)]
	return all_paths
	
imagenames = getallpaths(paths)

# Generate thumbnail images and find the intensity means of all 32x32 patches inside of the images
x=128
y=128
patchSize=32
numOfPatch = (x*y)/(patchSize*patchSize)
avgArray=[[]]
imgArray=[]
for i,image in enumerate(imagenames):
	file, ext = os.path.splitext(image)
	im = Image.open(image)
	if ext == '.jpg':
		im = im.convert('RGB')
	im = im.resize((x,y), Image.ANTIALIAS)
	imgArray.append(im)
	avgArray.append([])

	for j in range(0,x,patchSize):
		for k in range(0,y,patchSize):
			box = (j,k,j+patchSize,k+patchSize)
			I=im.crop(box)
			avgArray[i].append(np.mean(I))

for i in range(0, len(imgArray)-1):
	for j in range(i+1, len(imgArray)):
		isSimilar = True
		for p in range(0,numOfPatch):
			if(abs(avgArray[i][p]-avgArray[j][p])>0):
				p=numOfPatch+1
				isSimilar = False
		if isSimilar:
			print(imagenames[i], imagenames[j])
