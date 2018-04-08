- 作业要求：在MiniSearchEngine的基础上实现BoolSearch的功能。
- 源代码地址：[https://github.com/piaoliangkb/Flaskblog/tree/master/app/extends](https://github.com/piaoliangkb/Flaskblog/tree/master/app/extends)
- 最终结果地址: [http://piaoliangkb.info/extends/boolsearch](http://piaoliangkb.info/extends/boolsearch)

![image.png](https://upload-images.jianshu.io/upload_images/11146099-c074e90839ee6803.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
-------------------------------------------------------------
### MiniSearchEngine实现方法

1. 首先建立一个MiniSearchEngine类，在类中定义两个方法，分别为++SearchSingleKeyword(data, isfound)++和++GenerateResultDict(occurset)++
2. ++SearchSingleKeyword(data,isfound)++ 方法传入要查询的单一单词和是否查找到的标志isfound，默认为True。若没查找到isfound返回False。

```
class MiniSearchEngine():
    @staticmethod
    def SearchSingleKeyword(data, isfound=True):
        occurset = set()
        # 初始化结果集合为空
        if data is not None:
            with open(basedir + "/wordindex.txt") as file:
                for line in file.readlines():
                    if data == line.split('\t')[0]:
                        # 如果在wordindex文件中有对应的单词
                        occurset = set(line.split('\t')[1].split())
                        # 将对应单词出现的文章索引号添加到occurset中
            if occurset:
                isfound = True
            else:
                isfound = False
                # 若未查找到结果，isfound返回False
        return occurset, isfound
```

3. ++GenerateResultDict(occurset)++ 函数根据查询出的occurset集合生成{文章名称：文章内容}列表进行展示。
```
@staticmethod
    def GenerateResultDict(occurset):
        queryresult = {}
        with open(basedir + "/documentindex.txt") as file:
            for line in file.readlines():
                for i in occurset:
                    if i == line.split('\t')[0]:
                        # 如果occurset集合中的元素对应文件索引中的索引值，则取出当前索引值对应的文件地址
                        resultpath = line.split('\t')[1].replace('\n', '')
                        # 索引对应的文件地址
                        with open(resultpath) as file:
                            filename = os.path.split(resultpath)[1]
                            # 文件名
                            queryresult[filename] = file.read()
                            # 文件名->文件内容对应字典
                        occurset.remove(i)
                        # 移除occurset中对应的值
                        break
        return queryresult
```

---------------------------------------------
### 在MiniSearchEngine的基础上添加bool查询的功能

1. 首先定义查询结果字典和isfound的默认值
```
queryresult = {}
# 查询结果字典
isfound = True
# 标记是否查询到结果，默认值设为True的原因是第一次进入界面时不显示未查找
``` 
2. 从网页上获取查询参数,如果只有一个参数，则直接使用MiniSearchEngine中的SearchSingleKeyword方法进行查询
```
query = request.args.get('query', None)
# 查询参数的获取
words = []
    if query:
        words = query.split()
        if len(words) == 1:
            occurset, isfound = MiniSearchEngine.SearchSingleKeyword(words[0], isfound)
            if occurset:
                queryresult = MiniSearchEngine.GenerateResultDict(occurset)
````
3. 如果有多个参数，则此时words列表中保存了所有的参数。建立一个新的列表resultlist保存 ++单词对应的索引集合++ 和 ++bool关键词++ 。  
4. 遍历words列表中的所有项，如果当前为第一项或者为最后一项，则把该项当成单词进行SearchSingleKeyword查找并将查找结果添加到resultlist中。如果不是第一项或者最后一项，则对于以下四种情况分别处理：  
                    **["AND", "AND"]**  
                    **["AND", set]**  
                    **[set, "AND"]**  
                    **[set, set]**  
- 如果前一个元素为bool算符，那么当前元素必定当作单词；  
- 如果前一个元素为集合，当前元素若为AND OR则为bool算符，否则当作单词。   
- 将当前元素添加到resultlist中
```
resultlist = []
            # 建立一个列表暂存“单词对应的索引集合信息”和“bool关键词”
            for i in range(len(words)):
                if i == 0 or i == len(words) - 1:
                    wordindexset, temp = MiniSearchEngine.SearchSingleKeyword(words[i])
                    resultlist.append(wordindexset)
                else:
                    """
                    对于以下四种情况分别处理：
                    "AND" "AND"
                    "AND" set
                    set "AND"
                    set set
                    如果前一个元素为bool算符，那么当前元素必定当作单词
                    如果前一个元素为集合，当前元素若为AND OR则为bool算符，否则当作单词
                    """
                    if type(resultlist[i - 1]) == str:
                        # 如果结果集中前一个元素为bool算符，则当前元素应该为集合
                        wordindexset, temp = MiniSearchEngine.SearchSingleKeyword(words[i])
                        resultlist.append(wordindexset)
                    else:
                        if words[i] == "or" or words[i] == "OR":
                            resultlist.append("OR")
                        elif words[i] == "and" or words[i] == "AND":
                            resultlist.append("AND")
                        else:
                            wordindexset, temp = MiniSearchEngine.SearchSingleKeyword(words[i])
                            resultlist.append(wordindexset)
```
5. 最后遍历resultlist集合，若遇到bool运算符则检查下一个元素，若为集合则检查前一个元素根据前一个元素的类型进行相应的处理。
- 如果两个集合之间没有bool算符，则该集合和前一个集合进行交操作，结果存到当前集合；
- 若前一个bool算符为AND，则该集合与AND之前的集合进行交操作，结果保存到当前集合；
- 若前一个bool算符为or，则该集合与OR之前的集合进行并操作，结果保存到当前集合。
- 最终的结果为最后一个集合。
```
            for i in range(1, len(resultlist)):
                # 只有遇到当前元素为indexset才进行处理，若遇到bool运算符则检测下一个元素
                if type(resultlist[i]) == type(resultlist[i - 1]):
                    # 如果两个集合同为set，即两个单词相邻的情况
                    # [set set]
                    resultlist[i] = resultlist[i - 1] & resultlist[i]
                elif type(resultlist[i - 1]) == str and type(resultlist[i]) == set:
                    # [AND set]
                    if resultlist[i - 1] == "AND":
                        resultlist[i] = resultlist[i] & resultlist[i - 2]
                    elif resultlist[i - 1] == "OR":
                        resultlist[i] = resultlist[i] | resultlist[i - 2]
            queryresult = MiniSearchEngine.GenerateResultDict(resultlist[-1])
```
----------------------------------------------------------
结果展示使用Python的Flask框架，完整代码请移步[https://github.com/piaoliangkb/Flaskblog/tree/master/app/extends](https://github.com/piaoliangkb/Flaskblog/tree/master/app/extends)

- \_\_init__.py    Flask蓝图注册
- mnisearchengine.py    MiniSearchEngine类
- invert.py    倒排索引和文章索引的建立
- views.py    Flask的视图文件

对应的html文件为template中的booleansearch.html

------------------------------------------------------
- 带有"and", "or"的布尔查询
![image.png](https://upload-images.jianshu.io/upload_images/11146099-420ecea4a0a2195a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 间隔词搜索
![image.png](https://upload-images.jianshu.io/upload_images/11146099-f190fd7fd2b99149.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 间隔词 + bool表达式
![image.png](https://upload-images.jianshu.io/upload_images/11146099-2d491df1a6f39a7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
------------------------------------------------------
欠缺：
1. 在进行bool查询时多建立了一个列表进行线性存储，数据结构以及查询方式有待改善。
2. 进行类似"most sports or scoring goals"查询的时候，根据bool表达式运算方式返回的结果只有((most and sports) or scoring) and goals的结果，是否与搜索的意愿相同需要考虑。