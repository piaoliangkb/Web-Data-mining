
### KMeans算法的简单实现

##### 1.大致思路
1. 随机选择K个点作为初始中心
2. 将剩余点归为距离他最近的中心点一类
3. 重新计算每一个聚类的中心
4. 重复2-3步直到收敛，即聚类的中心不再改变


##### 2.实现
1. 首先定义一个两个列表，分别保存VectorID和Vector
```
pathOfsamples = "samples.txt"
# 保存vector的id信息
sampleIds = []
# 保存vector
sampleVectors = []
# vecxtor的数量
numOfvectors = 0
```
2. 定义readSamples函数，将文件中的vector读到内存中
```
def readSamples(self):
	with open(self.pathOfsamples) as file:
		lines = file.readlines()
		for line in lines:
			line = line.split()
			# 当vectorid添加到sampleID中
			self.sampleIds.append(int(line[0]))
			# 当前行的向量添加到sampleVector中
			thislinevector = []
			for i in range(1,len(line)):
				thislinevector.append(float(line[i]))
			self.sampleVectors.append(thislinevector)
	self.numOfvectors = len(self.sampleIds)
```
3. 定义函数doClustering(numOfk)，其中参数为KMeans算法中唯一的参数K，即要分类的种类数。首先从已经存在的N个点中选出K个点，将他们的向量信息存储到centroids中。接着将起始选择的K个点的向量信息，K，和收敛阈值当作参数传递给函数kMeanClustering
```
def doClustring(self, numberOfK):
	# 保存聚类中心的向量信息
	centroids = []
	while True:
		# 从vector的编号中随机选取一个
		randpicknum = random.randint(0, len(self.sampleVectors)-1)
		# 如果该点已经被选中，则跳过进行下一次循环
		if self.sampleVectors[randpicknum] in centroids:
			continue
		# 如果没有被选中将该店添加到点集中
		centroids.append(self.sampleVectors[randpicknum])
		print("Sample " + str(randpicknum) + " is picked as an initial centroid.")
		if len(centroids) == numberOfK:
			break
	self.kMeanClustering(centroids, numberOfK, 0.00000001)
```
4. 定义函数kMeanClustering(centroids, numofClustering, ConvergThresh)，其中参数分别表示的意思为中心点集，聚类的数量(k)，收敛阈值。
- 多次执行函数kmeanClustering，每次执行都是一次迭代，获得一个新的中心点的结果，直到最后收敛。
- clusters 为每类点的索引号的集合，初始化为聚类的个数个空集，即
    

    clusters = [[] for i in range(numberOfClustering)]
- 对向量列表中的所有向量进行遍历，找到距离其最近的中心点，将其分到对应的类中。
- 分类完成后计算新的聚类中心和中心点改变的幅度。求中心：加起来平均；求改变幅度：新的中心和原中心的欧式距离。
欧式距离计算公式：
![](https://upload-images.jianshu.io/upload_images/11146099-1926e1afe731b1a5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


    	def getEuclideanDistance(self, vec1, vec2):
		summ = sum(math.pow(vec1[i] - vec2[i], 2) for i in range(len(vec1)))
		return math.sqrt(summ)

- 对新得到的中心点重复使用kMeanClustering函数，直到中心点的改变幅度收敛。

```
def kMeanClustering(self, centroids, numberOfClustering, ConvergThresh):
	print("This is a new iteration::::::::::::::::::::::::::::::::::::::::")
	# 将当前所有点归入到相应的分类中
	# 共有numberOfClustering 个聚类，初始化每个聚类为空
	clusters = [[] for i in range(numberOfClustering)]
	for i in range(self.numOfvectors):
		# 遍历所有向量列表中的向量，找出距离他最近的聚类点
		samplevec = self.sampleVectors[i]
		minndis = float('inf')
		mindisindex = -1
		for j in range(numberOfClustering):
			dis = self.getEuclideanDistance(samplevec, centroids[j])
			if dis < minndis:
				minndis = dis
				mindisindex = j
		clusters[mindisindex].append(i)
		print("Sample " + str(i) + " is assigned to cluster " + str(mindisindex))

	# 计算新的聚类中心
	newCentroids = []
	# 中心点的改变
	change = 0 
	for i in range(numberOfClustering):
		# 当前聚类的新中心的向量表示
		newCentroidsOfthisClustering = [0 for i in range(len(centroids[i]))]
		memberOfcluster = len(clusters[i])
		# 对当前聚类中的每个点
		for j in range(len(clusters[i])):
			for m in range(len(newCentroidsOfthisClustering)):
				# cluster[i][j]存着第i个聚类中第j个点的编号
				newCentroidsOfthisClustering[m] += self.sampleVectors[clusters[i][j]][m] /memberOfcluster
		change += self.getEuclideanDistance(centroids[i], newCentroidsOfthisClustering)
		newCentroids.append(newCentroidsOfthisClustering)
	print("change:" + str(change))

	if change>ConvergThresh:
		self.kMeanClustering(newCentroids, numberOfClustering, ConvergThresh)
	else:
		for i in range(len(newCentroids)):
			print("Now the centroids of the points is [{},{}]".format(newCentroids[i][0], newCentroids[i][1]) )

```

#### 3.程序执行结果
![](https://upload-images.jianshu.io/upload_images/11146099-be911cacd273bb76.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
---------------------------------------------
##### result
![](https://upload-images.jianshu.io/upload_images/11146099-d0f70f19cd050e79.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到三次执行之后，在K=2的情况下，程序最终两个中心点的结果和聚类的结果是相同的。

![](https://upload-images.jianshu.io/upload_images/11146099-576aa183d87d39a0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在K=3的情况下，四次执行出现了三次结果。由于随机选点，KMeans算法值保证了局部最优解，却无法保证全局最优。