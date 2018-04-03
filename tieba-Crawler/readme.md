

#### 百度贴吧图片爬虫

###### 基本思路：
- 使用BeautifulSoup+requests库进行html文本的获取和解析。
- 在帖子的首页寻找到帖子总页数爬取下来


    r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	pagenum = soup.find("li", class_="l_reply_num").find_all("span", class_="red")[1].text
	
在html文件中找到页数对应的标签，使用soup对象的find方法提取页号存入pagenum中。
- 找到不同页面的url规律：


    url=baseurl+ "?pn" + pagenum
- 标签名为"img",类名为"BDE_image"为我们所需要的图片


    pics = soup.find_all("img", class_="BDE_Image")
    
###### 完整程序：


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
    		
###### 爬取结果

截至帖子更新至3月14日下午，从帖子上共爬取1582张图片。  

![image.png](https://upload-images.jianshu.io/upload_images/11146099-dfd7577636a4316b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/11146099-a2660fa909d0356a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

    
