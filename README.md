# Rake_For_Chinese
A Python implementation of the Rapid Automatic Keyword Extraction (RAKE) algorithm as described in: Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. In M. W. Berry & J. Kogan (Eds.), Text Mining: Theory and Applications: John Wiley & Sons.
Codebase in MIT License

# Requirement
This package requires the Chinese text segmentation package Jieba. `pip install jieba` to install Jieba. Code is implemented in Python 3.6.5

# Primary Function
Use RAKE algorithm to extract Keywords from Chinese text. 
RAKE Keyword Extraction is an algorithm that is by design corpus-independent and language-independent. In a nutshell, it calculates scores for words based on its independent occurrence and its occurrence in phrases, and then combine all scores for every word inside a phrase to get the score for the phrase, with some additional criterias to eliminate boundary conditions.
This method however, cannot be directly applied to Chinese since first, there are no obvious word deliminators and second when we come to parsing phrases, there's more variety to it than that in English and other language with similar syntaxes.

## Functional Overview
Generation of "Word" and "Phrases" as needed by RAKE algorithm sought help from another Chinese Text Segmentation package, Jieba. Jieba is used to cut raw texts into segments of word. Then the list is filter with PoS property, stopword and conjunction word list and punctuation list to parse phrases. 
