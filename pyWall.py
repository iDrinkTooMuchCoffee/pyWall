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

# setup default naming convention.
# TODO: allow custom filenames and directories through argparse
nowTime = str(datetime.datetime.now().time()).replace(':', '.')
defaultSave = "cc_" + str(datetime.datetime.now().date()) + "_" + nowTime + ".png"
imgDir = str(os.getcwd()) + "\\" + defaultSave

category = "" # user input category string
catNum = "111" # category number code according to wallhaven
resolution = "1920x1080"
res_type = "resolutions" # defaults to exact resolution
ratio = "16x9"
linkArray = []


#TODO: allow choosing of sorting
#url = 'https://alpha.wallhaven.cc/search?categories=' + catNum + '&purity=100&' + res_type + '=' + resolution + '&ratios=' + ratio + '&sorting=favorites&order=desc&page='
url = 'https://alpha.wallhaven.cc/search?categories=' + catNum + '&purity=100&' + res_type + '=' + resolution + '&ratios=' + ratio + '&sorting=random&order=desc&page='
page = randint(1,15)
endpoint = url + str(page)

r = requests.get(endpoint)
soup = BeautifulSoup(r.content, 'html.parser')

# handle argument inputs
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="directory to save files in")
parser.add_argument("-c", "--category", help="category to search in. Valid options: general, people, anime, all")
parser.add_argument("-r", "--resolution", help="Desired exact resolution. Defaults to 1920x1080. Example usage: -r 2560x1440")
parser.add_argument("-rp", "--resolution_plus", help="At least this resolution. Defaults to 1920x1080. Example usage: -r 2560x1440")
parser.add_argument("-ar","--aspect-ratio", help="desired aspect ratio. Defaults to 16:9. Example usage: -ar 16x9")
args = parser.parse_args()

print("Parameters:")

def main():
	ParseArgs()
	ParsePage()

	i = randint(0,len(linkArray)-1)
	imagePage = linkArray[i]

	ParseImage(imagePage)

	# set current wallpaper to the downloaded image
	SPI_SETDESKWALLPAPER = 20
	ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imgDir, 0)
	print("Success.")
	print("Image saved to: " + str(imgDir))

def ParseArgs():
	if args.category:
		category = args.category 
		print("\tCategory: " + category)

	if args.resolution:
		res_type = "resolutions"
		resolution = args.resolution
		print("\tResolution: Exact " + resolution)

	if args.resolution_plus:
		res_type = "atleast"
		resolution = args.resolution_plus
		print("\tResolution: At least " + resolution)

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


def DownloadImage(link):
	print("downloading image...")
	response = requests.get(link)
	if response.status_code == 200:
		f = open(str(imgDir), 'wb')
		f.write(response.content)
		f.close()

# scrapes a random page in the random section
# returns an array made up of urls from the scraped page
def ParsePage():
	print("Choosing a random wallpaper...")
	for link in soup.find_all("a"):
		href = link.get("href")
		if not href:
			continue
		#if "favorites" in href:
		if "random" in href:
			continue
		if "thumbTags" in href:
			continue
		if "/w/" not in href:
			continue
		linkArray.append(href)

# get the direct image link for the wallpaper
def ParseImage(imagePage):
	r = requests.get(imagePage)
	print("imagepage: " + str(imagePage))
	soup = BeautifulSoup(r.content, 'html.parser')
	print("retrieving image link...")
	links = soup.find_all('img')
	for image in links:
		if "/full/" in image['src']:
			DownloadImage(image['src'])

if __name__ == "__main__":
	main()
