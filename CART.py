# -*- coding: utf-8 -*-
"""
@author: swx
"""

my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

class TreeNode:
    def __init__(self,col=-1,value=None,results=None,trueNode=None,falseNode=None):
        """
        col 是:某一维度
        value:维度的取值
        trueNode和falseNode都是TreeNode分别表示为ture和false时候的分支
        results:字典
        """
        self.col = col
        self.value = value
        self.results = results
        self.trueNode = trueNode
        self.falseNode = falseNode
def divideSet(rows,column,value):
     """
     按照某一列进行数据集拆分，需要考虑到的是表标称性属性和数值型属性
     column:某一列
     value:column这一列的取值
     """
     split_function = None#匿名函数
     if isinstance(value,int) or isinstance(value,float):
         split_function = lambda row:row[column] >= value
     else:
         split_function = lambda row:row[column] == value
         
     set1 = [row for row in rows if split_function(row)]
     set2 = [row for row in rows if not split_function(row)]
     return (set1,set2)
def uniqueCounts(rows):
    """
    某一类别标签出现的次数
    """
    results = {}
    for row in rows:
        #类标签在最后一个维度
        label = row[len(row) - 1]
        if label not in results:
            results[label] = 0
        results[label] += 1
    return results
def giniImpurity(rows):
    """
    基尼指数,值越大越不好
    """
    total = len(rows)
    results = uniqueCounts(rows)
    value = 0
    for l1 in results:
        v1 = float(results[l1]) / total
        for l2 in results:
            if l1 == l2:
                continue
            v2 = float(results[l2]) / total
            value += v1*v2
    return value
def entropy(rows):
    """
    信息熵:越大表示越混乱
    """
    from math import log
    log2 = lambda x : log(x) / log(2) #以2为底数
    results = uniqueCounts(rows)
    #开始计算
    ent = 0.0
    for label in results.keys():
        p = float(results[label]) / len(rows)
        ent -= p * log2(p)
    return ent
    
def buildTree(rows,score = entropy):
    """
    score:entropy or giniImpurity
    """
    if len(rows) == 0:
        return TreeNode()
    #计算父集合的信息熵
    current_score = score(rows)
    #临时变量，存储信息
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    
    column_count = len(rows[0]) - 1
    for col in range(0,column_count):#col int 类型
        #每一维度的取值
        column_values = {}
        for row in rows:  
            column_values[row[col]] = 1 #找出所有的取值
        #对每一个维度的取值进行拆分
        for value in column_values.keys():
            (set1,set2) = divideSet(rows,col,value)
            #接下来计算信息增益
            p = float(len(set1)) / len(rows)
            gain = current_score - p * score(set1)-(1 - p)*score(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col,value) # 特征和值
                best_sets = (set1,set2) #set1 是true，set2是false
    #递归方式创建子分支
    if best_gain > 0:
        trueBranch = buildTree(best_sets[0])
        falseBranch = buildTree(best_sets[1])
        return TreeNode(col=best_criteria[0],value=best_criteria[1],
                trueNode = trueBranch,falseNode = falseBranch)
    else: #信息增益为0或负数，表明应该停止分割，该节点为叶节点，叶节点的results不为空
        return TreeNode(results=uniqueCounts(rows))
        
#print tree
def printTree(tree,indent=''):
    if tree.results != None:#如果不是叶子节点
        print str(tree.results)
    else:
        print str(tree.col)+':'+str(tree.value)+'? '
        #打印分支
        print indent + 'T->'
        printTree(tree.trueNode,indent + "  ")
        print indent + "F->"
        printTree(tree.falseNode,indent + "  ")
#------------二叉树的操作--------------
#这种方法错误，因为叶子节点左右节点为None，result不为None
def getWidth1(tree):
    if tree == None:
        return 0
    return getWidth(tree.trueNode) + getWidth(tree.falseNode) + 1
def getWidth(tree):
    if tree.trueNode == None and tree.falseNode == None:
        return 1
    return getWidth(tree.trueNode) + getWidth(tree.falseNode)
def getDepth(tree):
    if tree.trueNode == None and tree.falseNode == None:
        return 0
    return max(getDepth(tree.trueNode),getDepth(tree.falseNode)) + 1
from PIL import  Image,ImageDraw

def drawTree(tree,jpeg='tree.jpg'):
    w = getWidth(tree) * 100
    h = getDepth(tree) * 100 +120
    #创建画布
    img = Image.new('RGB',(w,h),(255,255,255))
    draw = ImageDraw.Draw(img)
    
    drawNode(draw,tree,w/2,20)
    img.save(jpeg,'JPEG')
def drawNode(draw,tree,x,y):
    if tree.results == None:
        w1 = getWidth(tree.trueNode) * 100#右子树
        w2 = getWidth(tree.falseNode) * 100
        #绘制当前节点
        draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))
        
        left = x - (w1 + w2) /2
        right = x + (w1 + w2) / 2
        #绘制连线
        draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100),fill=(0,255,0))
        #绘制分支节点
        drawNode(draw,tree.trueNode,right-w2/2,y+100) #右
        drawNode(draw,tree.falseNode,left+w1/2,y+100) #左
    else:
        txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
        draw.text((x-20,y),txt,(0,0,0))
#为新的数据分类
def classify(sample,tree):
    """
    递归方法遍历决策树，输出叶子节点
    """
    if tree.results != None:#说明这个树只有一个叶子节点
        return tree.results
    else:
        v = sample[tree.col]
        branch = None
        if isinstance(v,int) or isinstance(v,float): #数值型
            if v >= tree.value:
                branch = tree.trueNode
            else:
                branch = tree.falseNode
        else: #标称型
            if v == tree.value:
                branch = tree.trueNode
            else:
                branch = tree.falseNode
    return classify(sample,branch)
#剪枝
def prune(tree,mingain):
    #如果分枝不是叶子
    if tree.trueNode.result == None:
        prune(tree.trueNode,mingain)
    if tree.falseNode.result == None:
        prune(tree.falseNode,mingain)
    #这部分没有实现
if __name__ == "__main__":
    #s1,s2 = divideSet(my_data,2,'yes')
    #print entropy(s1)
    #print giniImpurity(s1)
    tree = buildTree(my_data)
    #printTree(tree)
    drawTree(tree,jpeg="111.jpg") #绘制决策树
    print getWidth(tree)
    print getDepth(tree)
    sample = ['(direct)','USA','yes',5]
    
    
         
            