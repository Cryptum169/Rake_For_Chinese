from src.Rake import Rake

obj = Rake()
stop_path = "data/stoplist/中文停用词表(1208个).txt"
conj_path = "data/stoplist/中文分隔词词库.txt"
obj.initializeFromPath(stop_path, conj_path)

path = 'data/testCase/文本1.txt'
result = obj.extractKeywordFromPath(path)
print(result)