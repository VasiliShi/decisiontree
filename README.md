##总结
### 决策树的节点
 在学习数据结构-二叉树部分的时候，这一部分与之前学的线性数据结构相比算是比较复杂的，因为它需要存储的结构比较多，需要对多个指针进行操作，本着学以致用的原则，我们试着为我们的决策树定义节点；
```Python
class TreeNode:
    def __init__(self,col=-1,value=None,results=None,trueNode=None,falseNode=None):
        self.col = col
        self.value = value
        self.results = results
        self.trueNode = trueNode
        self.falseNode = falseNode
```
解释以下成员变量：
   - col:待验证的条件，就是这一特征维度所在特征集合中的index，默认为-1
   - value：特征的取值，与col变量相对应
   - trueNode和falseNode：都是TreeNode类型，表示决策数的左右节点，表示是否属于value这一特征
   - results：字典类型，key为最终的类别标签，value这一类别的个数
### 拆分数据
这份代码使用的是CART的算法，为了构造决策树，算法首先创建一个根节点，然后通过数据集中的所有观测变量，从中选择出最合适的变量对数据集进行拆分，下面这段代码的功能就是拆分成两个数据集，第一个数据集包含与指定的参考值相匹配，第二个数据集包含不匹配的剩余数据集
```Python
def divideSet(rows,column,value):
     split_function = None#匿名函数
     if isinstance(value,int) or isinstance(value,float):
         split_function = lambda row:row[column] >= value
     else:
         split_function = lambda row:row[column] == value
         
     set1 = [row for row in rows if split_function(row)]
     set2 = [row for row in rows if not split_function(row)]
     return (set1,set2)
```
这段代码之所以这么设计是有一定依据的，因为我们的样本特征维度的数值类型是不能确定的`数值型`和`标称型`,如果是标称型那好办，如果是数值型那就需要对其离散化了。其中使用`匿名函数`也是一个很好的方法。
### 特征选择的指标
决策树常用的特征选择指标有`信息增益`,`基尼系数等`理论部分这里就不在赘述，具体实现请看代码
### 构造决策树
二叉树的构建是一个递归的过程，决策树亦如此，它通过为`当前数据集合选择最合适的拆分条件来实现决策树的构建过程`；信息增益为0或负数，表明应该停止分割，该节点为叶节点，叶节点的results不为空，具体实现参看代码`buildTree`方法，代码给出了详细的注释
### 二叉树的操作
学习数据结构的时候，经常会遇到树的遍历，什么求高度宽度呀啥玩意的，傻傻分不清。主要是教学的内容太抽象，没有应用到实际中，所以理解的就不够到位。这里我就填下大学时候留下的坑，决策树的宽度和深度，其实很简单的操，重在理解
```Python
def getWidth(tree):
    if tree.trueNode == None and tree.falseNode == None:
        return 1
    return getWidth(tree.trueNode) + getWidth(tree.falseNode)
def getDepth(tree):
    if tree.trueNode == None and tree.falseNode == None:
        return 0
    return max(getDepth(tree.trueNode),getDepth(tree.falseNode)) + 1
```
