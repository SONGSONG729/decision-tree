import matplotlib.pyplot as plt
from pylab import mpl

# 用以显示中文
mpl.rcParams['font.sans-serif'] = ['FangSong']

'''
使用文本注解绘制树节点
'''
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.axl.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                            textcoords='axes fraction', va="center", ha="center",
                            bbox=nodeType, arrowprops=arrow_args)

def createPlot():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.axl = plt.subplot(111, frameon=True)
    plotNode('决策节点', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode('叶节点', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.switch_backend('agg')
    plt.show()

def getNumLeafs(myTree):
    '''
    遍历整棵树，累计叶子节点的个数，并返回该值
    :param myTree:
    :return:
    '''
    numLeafs = 0
    # in the py3, type(myTree.keys()) is dict_keys.
    # It can be directed used for iteration, but index is not suitable.
    # in the py2, type(myTree.keys()) is list.
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    '''
    计算遍历过程中遇到判断节点的个数
    :param myTree:
    :return:
    '''
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                   ]
    return listOfTrees[i]

def plotMidText(cntrPt, parentPt, txtString):
    '''
    在父子节点间填充文本信息
    :param cntrPt:
    :param parentPt:
    :param txtString:
    :return:
    '''
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    createPlot.axl.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
    '''
    绘制树形图
    plotTree.xOff、plotTree.yOff：全局变量，追踪已绘制的节点位置
    :param myTree:
    :param parentPt:
    :param nodeTxt:
    :return:
    '''
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)  # 计算宽与高
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)  # 标记子节点属性值
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  # 减少y偏移，自顶向下绘制图形，一次递减y的坐标
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff),cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


def createPlot(inTree):
    '''
    创建绘图区，计算树图形的尺寸，并调用递归函数plotTree()
    :param inTree:
    :return:
    '''
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.axl = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()
