from tokenize import String
from node import Node, OrNode, LeafNode, PlusNode, QuestionNode, StarNode, ConcatNode
from tree import SyntaxTree
import graphviz



def graph(tree:SyntaxTree, graphName:String, fileName):
    s = graphviz.Digraph(str(graphName), filename=fileName, node_attr={'shape': 'plaintext'}, format='svg')
    recursiveGraph(s,tree.root,[0])

    s.node("Regex",graphName)


    #Create table of follow positions
    startTable = '''<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> 
                <TR> <TD>Node</TD> <TD>Follow positions</TD> </TR>'''
    data = ""
    endTable = '''</TABLE>>'''

    index = 1    
    for x in tree.followpos:
        data+='''<TR> <TD>%s</TD> <TD>%s</TD> </TR>'''%(str(index),str(x))
        index+=1

    s.node("Table of follow positions",startTable+data+endTable)

    
    s.view()

def recursiveGraph(s:graphviz.Digraph, node:Node, nodeNumber):

    nodeName = "node" + str(nodeNumber)
    nodeNumber[0]+=1
    symbol = ""

    if isinstance(node,ConcatNode):
        symbol="."
    elif isinstance(node,OrNode):
        symbol="|"
    elif isinstance(node,StarNode):
        symbol="*"
    elif isinstance(node,PlusNode):
        symbol="+"
    elif isinstance(node,QuestionNode):
        symbol="?"
    elif isinstance(node,LeafNode):
        symbol=node.string
    else:
        symbol="error"

    s.node(nodeName, '''<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR>
                <TD PORT="f1">%s</TD>
                <TD PORT="f2">%s</TD>
                <TD PORT="f3">%s</TD>
            </TR>
            </TABLE>>'''%(str(node.firstpos),str(symbol),str(node.lastpos)))

    if isinstance(node,ConcatNode) | isinstance(node,OrNode):
        s.edge(nodeName+":f2",recursiveGraph(s,node.lchild,nodeNumber)+":f2")
        s.edge(nodeName+":f2",recursiveGraph(s,node.rchild,nodeNumber)+":f2")            
    elif isinstance(node,StarNode) | isinstance(node,PlusNode) | isinstance(node,QuestionNode):
        s.edge(nodeName+":f2",recursiveGraph(s,node.child,nodeNumber)+":f2")    
    

    return nodeName