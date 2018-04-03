import requests
from bs4 import BeautifulSoup
import os

baseurl = "https://tieba.baidu.com/p/5461479002"
index = 1

def getpics(url):
	global index
	r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	pagenum = soup.find("li", class_="l_reply_num").find_all("span", class_="red")[1].text
	pics = soup.find_all("img", class_="BDE_Image")
	for pic in pics:
		#print(pic['src'])
		savepics(pic['src'], index)
		print("picture " + str(index) +" saved")
		index = index+1
	
def savepics(url, name):
	if os.path.exists('pictures/picture'+str(name)+'.jpg'):
		return 
	if not os.path.exists('pictures'):
		os.mkdir("pictures")
	else:
		piccontent = requests.get(url).content
		with open('pictures/picture'+str(name)+'.jpg','wb') as f:
			f.write(piccontent)

if __name__ == '__main__':
	r = requests.get(baseurl)
	soup = BeautifulSoup(r.text,"lxml")
	pagenum = soup.find("li", class_="l_reply_num").find_all("span", class_="red")[1].text
	for i in range(1, int(pagenum)+1):
		if(i==1):
			url = baseurl
		else:
			url = baseurl + "?pn=" + str(i)
		getpics(url)
