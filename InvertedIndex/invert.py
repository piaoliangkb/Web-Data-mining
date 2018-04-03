import os

class InvertedFile():
    @staticmethod
    def BuildDocumentIndex(path):
        index = 1
        with open("listdir.txt", "w") as f:
            for filename in os.listdir(path):
                f.write(str(index) + "\t" + os.path.join(path, filename) + "\n")
                index = index + 1

    @staticmethod
    def BuildWordIndex():
        WordDir = {} # 建立字典保存单词和文章编号列表的对应关系
        with open("listdir.txt") as f:
            for line in f:
                fileindex = line.split('\t')[0]
                filepath = line.split('\t')[1].replace('\n', '')
                with open(filepath) as file:
                    filecontent = file.read() # 读出文件中所有内容，返回string
                    filecontent = filecontent.replace('[', '').replace(']', '').replace('.', '').replace(',', '').replace('"', '')
                    for i in range(10):
                        filecontent = filecontent.replace(str(i), '')
                    filecontent = filecontent.split() # 不带参数的split会处理所有空格，返回一个list
                    for item in filecontent:
                        if item in WordDir.keys():
                            WordDir[item].append(fileindex)
                        else:
                            WordDir[item] = [fileindex]
        with open("wordindex.txt", "w") as f:
            for item in WordDir.keys():
                f.write(item + '\t')
                for i in WordDir[item]:
                    f.write(i + ' ')
                f.write('\n')

if __name__ == '__main__':
    path = r"D:\documents\大三下\webdatamining\倒排索引\倒排索引\documents"
    if not os.path.exists("listdir.txt"):
        InvertedFile.BuildDocumentIndex(path)
    InvertedFile.BuildWordIndex()


