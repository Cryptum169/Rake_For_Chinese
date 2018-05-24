# Rake_For_Chinese
A Python implementation of the Rapid Automatic Keyword Extraction (RAKE) algorithm as described in: Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. In M. W. Berry & J. Kogan (Eds.), Text Mining: Theory and Applications: John Wiley & Sons.
Codebase in MIT License

# Requirement
This package requires the Chinese text segmentation package Jieba. `pip install jieba` to install Jieba. Code is implemented in Python 3.6.5

# Primary Function
Use RAKE algorithm to extract Keywords from Chinese text. 

## Functional Overview
RAKE Keyword Extraction is an algorithm that is by design corpus-independent and language-independent. In a nutshell, it calculates scores for words based on its independent occurrence and its occurrence in phrases, and then combine all scores for every word inside a phrase to get the score for the phrase, with some additional criterias to eliminate boundary conditions.
This method however, cannot be directly applied to Chinese since first, there are no obvious word deliminators and second when we come to parsing phrases, there's more variety to it than that in English and other language with similar syntaxes.
Generation of "Word" and "Phrases" as needed by RAKE algorithm sought help from another Chinese Text Segmentation package, Jieba. Jieba is used to cut raw texts into segments of word. Then the list is filter with PoS property, stopword and conjunction word list and punctuation list to parse phrases. 

## Sample Output
Take news article at this link for example: http://www.pingwest.com/sony-expo-2018-at-chengdu/
Sample output in the following, with the output of this implementation in the last line

```
TextRank4ZH-关键词：
索尼, 索粉, 粉丝, 上, 业务, 破产, sony, 人, 会, 产品
jieba-关键词：
平井, 一夫, 粉丝, 魅力, 产品, 中国, 业务, 财年, 偶像, 成都
KeyExtract-关键词：
索尼, 索粉, 平井, 一夫, 魅力, 一个, 财年, 粉丝, 赏, 亿日元
TextRank4ZH-关键词：
平井一夫, 索尼魅力, 索尼中国
jieba-关键短语：(N/A)
KeyExtract-关键短语：（N/A）
Rake4ZH-关键短语：
名字——索尼魅力赏, 游戏作品软件销量, 高质量消费电子品产, 索尼游戏业务正式回, 放心——,  游戏销量超,  全球销量超,  款精品 , 款游戏作品, 伙伴合作补完
Rake 中文关键短语/词
平井一夫, 营业利润, 游戏, 正式, 明星, 总裁, 改革, 高桥洋, 中国, 利润
```
