# Text-Mining

This code can be used to assign keywords to documents and find association rules between words from database of documents. Further, with little modifications one can create a document suggestion system using search keywords.

### Getting Started

* Clone this repository 
* Execute **textMining.py**
* You will be asked **support** and **confidence** value. Ones you enter those, you'll get the association rules as output.
* That's pretty much it. Good Job!

### Prerequisites

Need to have python 3.6 installed on your machine.

## Running the tests

* The code is written in such a way that when you execute TextMining.py, it will check for the folder named **documentDatabase** and read all the **.txt** files in it. Each text file acts as a separate document. Since the input of the code should be database of documents, we have multiple documents in **documentDatabase** folder.
* Ones all the documents are read, they are cleaned by removing stop words. A word is further cleaned using stemming. A list of stop words can be found in **listOfStopWords.txt**
```
Example of stemming: fill, filled, filling can be interpreted as fill
```
* Further, each document is assigned few keywords using **tf-idf** algorithm. Keywords are written in a file named **aprioriInput.txt** 
At last **Apriori Algorithm takes** on the work. It reads **aprioriInput.txt** and generate association rules based on **Minimum Support** and **Minimum Confidence**
* **Minimum Support:** A minimum support is applied to find all frequent itemsets in a database.
* **Minimum Confidence:** A minimum confidence is applied to these frequent itemsets in order to form rules.


## Built With

* [Python 3.6](https://www.python.org/downloads/release/python-360/)


Fork the repo and try to come up with some optimized version of the algorithm.

## Author

* [Jeet Patel](https://github.com/MrPatel95)


#### Social
It is crucial to stay social ;)
* [LinkedIn](https://www.linkedin.com/in/jeet-patel-13aa27113/)
* [Instagram](https://instagram.com/gujju.chokro/)
