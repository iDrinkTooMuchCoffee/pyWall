# Dependencies

1. [Python 3](https://www.python.org/downloads/)
2. [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
3. [Requests](http://docs.python-requests.org/en/master/)

---
# Usage

When running the script, you can pass 2 potential arguments:

1. **Category**

	- The category that the script will search in for your image.
	- Valid categories are `General`, `People`, and `Anime`.
	- When the argument is left blank, the search includes all 3 categories.

2. **Save Directory**

	- The directory in which to save the image.
	- When left blank, it will save in the local directory of the script.
	- This argument can also be used to just apply a filename, while saving it in the local directory. For example,
		
        `pyWall.py General image1`
        
        This will save the image as 'image1.png' in the local directory.

---
To have a new wallpaper on every boot (win 10):

Bring up the 'run' menu by pressing `win` + `R` on your keyboard and enter `shell:startup` to open the 'Startup' folder. Drop the script in this folder and it will run on every boot, giving you a new wallpaper every time.
