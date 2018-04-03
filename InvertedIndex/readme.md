
- 建立倒排索引思路：
1. 首先遍历文章所在文件路径，建立文章的索引。
2. 使用Python中的字典存储单词和对应文章索引号的信息。初始时建立一个空字典。
3. 根据文章索引中文章的位置，打开每一个文章，去除单词之外的字符后生成一个单词列表。对列表中的所有元素进行遍历，如果元素在字典中，则将对应的文章索引号添加到value中的列表；否则在字典中添加一个新的元素，初始化一个列表并添加进文章的索引号。
4. 工作完成。

- 代码：
```
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

```

- 代码解释：
1. 使用Python中的os模块进行路径的处理
2. BuildDocumentIndex()函数浏览所有文章并存储文章的路径和对应的索引号。
3. BuildWordIndex()函数中首先建立一个名为WordList的空字典，接着打开上一步建立的DucomentIndex文件，根据文件的路径读出文件中的信息，处理得到单词存入WordList中。最后将WordList中的内容写出到文件WordIndex。

- 结果：

![image.png](https://upload-images.jianshu.io/upload_images/11146099-8319341d51ff3ef5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/11146099-9c3e1a7c67810135.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)