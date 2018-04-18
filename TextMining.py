from nltk.stem import PorterStemmer
import os
import string
from collections import Counter
import math
from operator import itemgetter
import time
from collections import OrderedDict
import itertools
start_time = time.time()


######################################################
''' Functions to find the keywords in the documents '''
######################################################

def createStopWords(filename):
    stopWords = []
    with open(filename, "r") as file_object:
        for line in file_object:
            stopWords.append(line.rstrip()) 
    return stopWords

def readFilesAndReturnCleanList(stopWords):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~/+-1234567890'''
    cleanDocuments = {}
    individualDocument = []
    for file in os.listdir("./documentDatabase"):
        if file.endswith(".txt"):
            documentName = os.path.join(file)
            with open("./documentDatabase/" + documentName, "r") as document:
                for line in document:
                    cleanLine = line.rstrip()
                    listofWordsInALine = cleanLine.split(" ")
                    cleanWord = ""
                    ps = PorterStemmer()
                    for word in listofWordsInALine:
                        if word.lower() not in stopWords:
                            word = ps.stem(word)
                            for letter in word:
                                if letter not in punctuations:
                                    cleanWord = cleanWord + letter
                            if (cleanWord != ""):
                                individualDocument.append(cleanWord)             
                            cleanWord = ""
                cleanDocuments[documentName] = individualDocument 
                individualDocument = [] 
    return cleanDocuments                            
        
def termFrequency(documentName, document):
    lengthOfDocument = len(document)
    wordInformation = []
    wordInfoDictionary = {} 
    documentAndWordInfo = {}
    wordCounter = Counter(document)
    if lengthOfDocument != 0:
        for word, repetation in wordCounter.items():
            frequency = repetation / lengthOfDocument
            # wordInformation.append(repetation)
            wordInformation.append(frequency)
            # wordInformation.append(lengthOfDocument)

            wordInfoDictionary[word] = wordInformation
            wordInformation = [] 
    documentAndWordInfo[documentName] = wordInfoDictionary
    return documentAndWordInfo

def findTermFrequency(documentsInADictionary):
    tf = []
    for documentName, document in documentsInADictionary.items():
        documentAndWordInfo = termFrequency(documentName, document)
        tf.append(documentAndWordInfo)
    return tf

def findInverseDocumentFrequency(listOfUniqueWords, documentsInADictionary, tf):
    idf = {}
    numberOfDocuments = len(documentsInADictionary)
    for word in listOfUniqueWords:
        for document, words in documentsInADictionary.items():
            if word in words:
                if word in idf:
                    idf[word] =  idf[word] + 1
                else:
                    idf[word] = 1
    for word, repetation in idf.items():
        idf[word] = math.log10(numberOfDocuments / repetation)

    return idf

def createUniqueWordsList(documentsInADictionary):
    listOfUniqueWords = []
    for document, words in documentsInADictionary.items():
        for word in words:
            if word not in listOfUniqueWords:
                listOfUniqueWords.append(word)
    return listOfUniqueWords

def tfIdf(tf, idf):
    tfIdfReturnDictionary = {}
    listForWordAndValue = []
    mainDocumentList = []

    for documentAndWords in tf:
        documentName = ""
        for document, wordsInfo in documentAndWords.items():
            documentName = document
            if len(wordsInfo) != 0:
                for word, wordTf in wordsInfo.items():
                    tfIdfValue = wordTf[0] * idf[word]

                    listForWordAndValue.append(word)
                    listForWordAndValue.append(tfIdfValue)
                    mainDocumentList.append(listForWordAndValue)
                    listForWordAndValue = []
        mainDocumentList = sorted(mainDocumentList, key=itemgetter(1), reverse=True)
        tfIdfReturnDictionary[documentName] = mainDocumentList
        documentName = ""
        mainDocumentList = []
    return tfIdfReturnDictionary

def createInputFileForAprioriAlgorithm(tf_idf, topN):
    count = 0
    writeToFile = open("aprioriInput.txt", "w") 
    for documentName, values in tf_idf.items():
        length = len(values[:topN])
        if len(values) != 0:
            for i in values[:topN]:
                count = count + 1
                if count == length:
                    writeToFile.write(i[0])
                else:
                    writeToFile.write(i[0] + ", ")
            count = 0
            writeToFile.write("\n")

######################################################
''' Apriori Algorithm functions '''
######################################################

def generateC1(dataSet):
    productDict = {}
    returneSet = []
    for data in dataSet:
        for product in data:
            if product not in productDict:
               productDict[product] = 1
            else:
                 productDict[product] = productDict[product] + 1
    for key in productDict:
        tempArray = []
        tempArray.append(key)
        returneSet.append(tempArray)
        returneSet.append(productDict[key])
        tempArray = []
    return returneSet

def generateFrequentItemSet(CandidateList, noOfTransactions, minimumSupport, dataSet, fatherFrequentArray):
    frequentItemsArray = []
    for i in range(len(CandidateList)):
        if i%2 != 0:
            support = (CandidateList[i] * 1.0 / noOfTransactions) * 100
            if support >= minimumSupport:
                frequentItemsArray.append(CandidateList[i-1])
                frequentItemsArray.append(CandidateList[i])
            else:
                eleminatedItemsArray.append(CandidateList[i-1])

    for k in frequentItemsArray:
        fatherFrequentArray.append(k)

    if len(frequentItemsArray) == 2 or len(frequentItemsArray) == 0:
        #print("This will be returned")
        returnArray = fatherFrequentArray
        return returnArray

    else:
        generateCandidateSets(dataSet, eleminatedItemsArray, frequentItemsArray, noOfTransactions, minimumSupport)

def generateCandidateSets(dataSet, eleminatedItemsArray, frequentItemsArray, noOfTransactions, minimumSupport):
    onlyElements = []
    arrayAfterCombinations = []
    candidateSetArray = []
    for i in range(len(frequentItemsArray)):
        if i%2 == 0:
            onlyElements.append(frequentItemsArray[i])
    for item in onlyElements:
        tempCombinationArray = []
        k = onlyElements.index(item)
        for i in range(k + 1, len(onlyElements)):
            for j in item:
                if j not in tempCombinationArray:
                    tempCombinationArray.append(j)
            for m in onlyElements[i]:
                if m not in tempCombinationArray:
                    tempCombinationArray.append(m)
            arrayAfterCombinations.append(tempCombinationArray)
            tempCombinationArray = []
    sortedCombinationArray = []
    uniqueCombinationArray = []
    for i in arrayAfterCombinations:
        sortedCombinationArray.append(sorted(i))
    for i in sortedCombinationArray:
        if i not in uniqueCombinationArray:
            uniqueCombinationArray.append(i)
    arrayAfterCombinations = uniqueCombinationArray
    for item in arrayAfterCombinations:
        count = 0
        for transaction in dataSet:
            if set(item).issubset(set(transaction)):
                count = count + 1
        if count != 0:
            candidateSetArray.append(item)
            candidateSetArray.append(count)
    generateFrequentItemSet(candidateSetArray, noOfTransactions, minimumSupport, dataSet, fatherFrequentArray)

def generateAssociationRule(freqSet):
    associationRule = []
    for item in freqSet:
        if isinstance(item, list):
            if len(item) != 0:
                length = len(item) - 1
                while length > 0:
                    combinations = list(itertools.combinations(item, length))
                    temp = []
                    LHS = []
                    for RHS in combinations:
                        LHS = set(item) - set(RHS)
                        temp.append(list(LHS))
                        temp.append(list(RHS))
                        #print(temp)
                        associationRule.append(temp)
                        temp = []
                    length = length - 1
    return associationRule

def aprioriOutput(rules, dataSet, minimumSupport, minimumConfidence):
    returnAprioriOutput = []
    for rule in rules:
        supportOfX = 0
        supportOfXinPercentage = 0
        supportOfXandY = 0
        supportOfXandYinPercentage = 0
        for transaction in dataSet:
            if set(rule[0]).issubset(set(transaction)):
                supportOfX = supportOfX + 1
            if set(rule[0] + rule[1]).issubset(set(transaction)):
                supportOfXandY = supportOfXandY + 1
        supportOfXinPercentage = (supportOfX * 1.0 / noOfTransactions) * 100
        supportOfXandYinPercentage = (supportOfXandY * 1.0 / noOfTransactions) * 100
        confidence = (supportOfXandYinPercentage / supportOfXinPercentage) * 100
        if confidence >= minimumConfidence:
            supportOfXAppendString = "Support Of X: " + str(round(supportOfXinPercentage, 2))
            supportOfXandYAppendString = "Support of X & Y: " + str(round(supportOfXandYinPercentage))
            confidenceAppendString = "Confidence: " + str(round(confidence))
            returnAprioriOutput.append(supportOfXAppendString)
            returnAprioriOutput.append(supportOfXandYAppendString)
            returnAprioriOutput.append(confidenceAppendString)
            returnAprioriOutput.append(rule)
    return returnAprioriOutput



#   Generating stop wordds from a list of words in a text file
stopWords = createStopWords("listOfStopWords.txt")

#   Reading all the files and creating a clean dictionary
documentsInADictionary = readFilesAndReturnCleanList(stopWords)

#   Getting all unique words
listOfUniqueWords = createUniqueWordsList(documentsInADictionary)

#   Term Frequency
tf = findTermFrequency(documentsInADictionary)

#   Finding Inverse Document Frequency (IDF)
idf = findInverseDocumentFrequency(listOfUniqueWords, documentsInADictionary, tf)

#   This function gives the final result
tf_idf = tfIdf(tf, idf)

#   User input for top N keywords
topN = input("Enter value of N: ")
topN = int(topN)

#   Create an input file for apriori algorithm
createInputFileForAprioriAlgorithm(tf_idf, topN)


#####################################################################################

minimumSupport = input('Enter minimum Support: ')
minimumConfidence = input('Enter minimum Confidence: ')

minimumSupport = int(minimumSupport)
minimumConfidence = int(minimumConfidence)

# minimumSupport = 10
# minimumConfidence = 10
nonFrequentSets = []
allFrequentItemSets = []
tempFrequentItemSets = []
dataSet = []
eleminatedItemsArray = []
noOfTransactions = 0
fatherFrequentArray = []


#   Reading the data file line by line
with open("aprioriInput.txt") as fp:
    lines = fp.readlines()

for line in lines:
    line = line.rstrip()
    dataSet.append(line.split(","))

noOfTransactions = len(dataSet)

#   This function is called only ones to generate first candidate list
firstCandidateSet = generateC1(dataSet)

#   This function is called recursively and also calls recursive function
frequentItemSet = generateFrequentItemSet(firstCandidateSet, noOfTransactions, minimumSupport, dataSet, fatherFrequentArray)

#   This function generates association rules
associationRules = generateAssociationRule(fatherFrequentArray)

#   This function gives the final output
AprioriOutput = aprioriOutput(associationRules, dataSet, minimumSupport, minimumConfidence)

#   Following code is just simply printing the output
counter = 1
if len(AprioriOutput) == 0:
    print("There are no association rules for this support and confidence.")
else:
    for i in AprioriOutput:
        if counter == 4:
            print(str(i[0]) + "------>" + str(i[1]))
            counter = 0
        else:
            print (i,end="")
        counter = counter + 1
