# _*_ coding:utf-8 _*_
from math import log
import operator
import matplotlib.pyplot as plt
import treePlotter

def calcShannonEnt(dataSet):
    '''
    计算给定数据集的香农公式
    :param dataSet:
    :return:
    '''
    numEntries = len(dataSet)
    labelCounts = {}
    # 为所有可能分类创建字典
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)  # 以2为底求对数
    return shannonEnt
def createDataSet():
    '''
    简单鉴定数据集
    :return:
    '''
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    '''
    按照给定特征划分数据集
    :param dataSet: 待划分的数据集
    :param axis: 划分数据集的特征
    :param value: 需要返回的特征值
    :return:
    '''
    retDataSet = []  # 创建新的lise对象，不修改原列表
    for featVec in dataSet:
        # 将符合特征的数据抽取出来
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    '''
    选择最好的数据集划分方式
    :param dataSet:
    :return:
    '''
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        # 创建唯一的分类标签列表
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)

        newEntropy = 0.0
        # 计算每种划分方式的信息熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        # 计算最好的信息增益
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    '''
    :param classList: 分类名称的列表
    :return: 出现次数最多的分类名称
    '''
    # key：classList中唯一值的数据字典
    # value：classList中每个类标签出现的频率
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    # 用operator操作键值排序字典
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    '''
    创建树
    :param dataSet: 数据集
    :param labels: 标签列表，包含数据集中所有特征的标签
    :return:
    '''
    # classList列表变量包含了数据集的所有类标签
    classList = [example[-1] for example in dataSet]
    # 所有的类标签完全相同则停止划分，返回该类标签
    # 第一个元素的值的数量等于整个列表的长度，即说明整个列表都是这个值，所以该数据集类别全部相同了
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 所有特征已经利用完，仍然不能将数据集划分成仅包含唯一类别的分组，返回出现次数最多的类别作为返回值
    # 所有特征已经利用完，只剩下标签列，仍然无法区分剩余样本，则采用“少数服从多数”的方案
    if len(dataSet[0]) == 1:
        return majorityCnt()

    bestFeat = chooseBestFeatureToSplit(dataSet)  # 当前数据集选取的最好特征
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}  # 存储树的所有信息
    # 得到列表包含的所有属性值
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    # 遍历当前选择特征包含的所有属性值，在每个数据集划分上递归调用函数createTree()，
    # 得到的返回值将被插入到字典变量myTree中，
    # 函数终止时，字典中将会嵌套很多代表叶子节点信息的字典数据
    for value in uniqueVals:
        subLabels = labels[:]  # 复制了类标签，并将其存储在新列表变量subLabels中
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    '''
    使用决策树的分类函数（递归函数）
    :param inputTree:
    :param featLabels:
    :param testVec:
    :return:
    '''
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)  # 将标签字符串转换为索引
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

def main():
    '''
    myDat, labels = createDataSet()
    print(myDat)
    print(calcShannonEnt(myDat))
    '''
    '''
    myDat, labels = createDataSet()
    print(myDat)
    print(splitDataSet(myDat, 0, 1))
    print(splitDataSet(myDat, 0, 0))
    '''
    '''
    myDat, labels = createDataSet()
    print(chooseBestFeatureToSplit(myDat))
    print(myDat)
    '''
    '''
    myDat, labels = createDataSet()
    myTree = createTree(myDat, labels)
    print(myTree)
    '''
    """
    myDat, labels = createDataSet()
    print(labels)
    myTree = treePlotter.retrieveTree(0)
    print(myTree)
    print(classify(myTree, labels, [1, 0]))
    print(classify(myTree, labels, [1, 1]))
    """
    '''
    myTree = treePlotter.retrieveTree(0)
    storeTree(myTree, 'classifierStorage.txt')
    grabTree('classifierStorage.txt')
    '''

    # with open('lenses.txt') as fr:
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLables = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = createTree(lenses, lensesLables)
    print(lensesTree)
    treePlotter.createPlot(lensesTree)




if __name__ == '__main__':
    main()
