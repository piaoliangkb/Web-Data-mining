import random
import math 

class myKMeans():

	pathOfsamples = "samples.txt"
	# 保存vector的id信息
	sampleIds = []
	# 保存vector
	sampleVectors = []
	# vecxtor的数量
	numOfvectors = 0

	def getEuclideanDistance(self, vec1, vec2):
		summ = sum(math.pow(vec1[i] - vec2[i], 2) for i in range(len(vec1)))
		return math.sqrt(summ)

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


if __name__ == '__main__':
	a = myKMeans()
	a.readSamples()
	a.doClustring(3)

