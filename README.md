# LWE-based-fuzzy-extractor
A Python implementation of LWE-based Fuzzy Extractor

代码仅包括模糊提取器的理论实现，本地运行需要自己处理模糊提取器输入，例如：人脸特征、指纹特征等。
	
  - Apon等人提出的基于LWE假设可重用模糊提取器（对数级纠错）[<sup>[1]</sup>](#refer-anchor-1)
		
  - Wen等人提出的基于LWE假设可重用模糊提取器（线性级纠错）[<sup>[2]</sup>](#refer-anchor-2)

输入需要服从特定分布以满足模糊提取器安全性，具体可见参考文献。<br/><br/>

考虑实际应用中随机源输入达不到Wen等人的模糊提取器构造中熵的要求，Wen18.py中加入了自定义的**熵增模块**见entropy_increase.png


# Reference
<div id="refer-anchor-1"></div>

  [1] Daniel Apon, Chongwon Cho, Karim Eldefrawy, and Jonathan Katz. Efficient, reusable fuzzy extractors from LWE. In International Conference on Cyber Security Cryptography and Machine Learning, pages 1–18. Springer, 2017.


<div id="refer-anchor-2"></div>

  [2] Yunhua Wen and Shengli Liu. Reusable fuzzy extractor from LWE. In Australasian Conference on Information Security and Privacy, pages 13–27. Springer, 2018.
