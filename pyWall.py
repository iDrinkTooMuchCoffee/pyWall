#! python3

import re
import os
import sys
import datetime
import requests
import urllib
import shutil
import argparse
import codecs
import ctypes
from random import randint
from bs4 import BeautifulSoup

category = "" # user input category string
imgDir = None
catNum = "111" # category number code according to wallhaven
resolution = "1920x1080"
res_type = "resolutions" # defaults to exact resolution
ratio = "16x9"

# handle argument inputs
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="directory to save files in")
parser.add_argument("-c", "--category", help="category to search in. Valid options: general, people, anime, all")
parser.add_argument("-r", "--resolution", help="Desired exact resolution. Defaults to 1920x1080. Example usage: -r 2560x1440")
parser.add_argument("-rp", "--resolution_plus", help="At least this resolution. Defaults to 1920x1080. Example usage: -r 2560x1440")
parser.add_argument("-ar","--aspect-ratio", help="desired aspect ratio. Defaults to 16:9. Example usage: -ar 16x9")
args = parser.parse_args()

print("Parameters:")

if args.directory:
	saveDir = "%s.png" % args.directory
	# unreliable way of checking if a full directory was given or just a filename
	if '\\' not in saveDir:
		imgDir = str(os.getcwd()) + "\\" + saveDir
	else:
		imgDir = saveDir
else:
	nowTime = str(datetime.datetime.now().time()).replace(':', '.')
	defaultSave = "cc_" + str(datetime.datetime.now().date()) + "_" + nowTime + ".png"
	saveDir = defaultSave
	imgDir = str(os.getcwd()) + "\\" + saveDir

if args.category:
	category = args.category 
	print("\tCategory: " + category)

if args.resolution:
	res_type = "resolutions"
	resolution = args.resolution
	print("\tResolution: At least " + resolution)

if args.resolution_plus:
	res_type = "atleast"
	resolution = args.resolution_plus
	print("\tResolution: Exact " + resolution)

if args.aspect_ratio:
	ratio = args.aspect_ratio
	print("\tAspect Ratio: " + ratio)

# set the url parameter based on category input
if category.lower() == "anime":
	catNum = '010'
elif category.lower() == "people":
	catNum = '001'
elif category.lower() == "general":
	catNum = '100'

url = 'https://alpha.wallhaven.cc/search?categories=' + catNum + '&purity=100&' + res_type + '=' + resolution + '&ratios=' + ratio + '&sorting=favorites&order=desc&page='
page = randint(1,15)
endpoint = url + str(page)
linkArray = []

def DownloadImage(link):
	print("downloading image...")
	response = requests.get('https:' + link)
	if response.status_code == 200:
		f = open(saveDir, 'wb')
		f.write(response.content)
		f.close()

# scrapes a random page in the favorites section
def ParseFavs():
	print("Choosing a random wallpaper...")
	links = []
	for link in soup.find_all("a"):
		href = link.get("href")
		if not href:
			continue
		if "favorites" in href:
			continue
		if "thumbTags" in href:
			continue
		if "wallpaper" not in href:
			continue
		links.append(href)
		linkArray.append(href)
	return links

# get the direct image link for the wallpaper
def ParseImage():
	print("retrieving image link...")
	for link in soup.find_all("meta"):
		cont = link.get("content")
		if not cont:
			continue
		if "wallpapers.wallhaven.cc/wallpapers" not in cont:
			continue
		DownloadImage(cont)


r = requests.get(endpoint)
soup = BeautifulSoup(r.content, 'html.parser')


i = randint(0,len(ParseFavs())-1)
imagePage = linkArray[i]

r = requests.get(imagePage)
soup = BeautifulSoup(r.content, 'html.parser')

ParseImage()

# set current wallpaper to the downloaded image
SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imgDir, 0)
print("Success.")
print("Image saved to: " + imgDir)
